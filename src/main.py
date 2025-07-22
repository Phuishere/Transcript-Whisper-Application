import os
import sys
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
import json
import re
import threading
import time

from pydub import AudioSegment
import whisper

from modules.audio_process import mp3_to_wav, chunk_wav_to_files

# Utils function
def get_base():
    try:
        base = sys._MEIPASS
    except AttributeError:
        base = os.path.abspath(".")
    return base
BASE = get_base()
TEMP_CONTAINER_DIR = os.path.join(BASE, "src/temp")

def get_ffmpeg_paths():
    return {
        "converter": os.path.join(BASE, "src/ffmpeg/ffmpeg.exe"),
        "ffprobe": os.path.join(BASE, "src/ffmpeg/ffprobe.exe"),
        "ffmpeg": os.path.join(BASE, "src/ffmpeg/ffmpeg.exe")
    }
ffmpeg_paths = get_ffmpeg_paths()
AudioSegment.converter = ffmpeg_paths["converter"]
AudioSegment.ffmpeg = ffmpeg_paths["ffmpeg"]

def get_subdirs(path) -> list:
    try:
        return [
            name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name))
        ]
    except FileNotFoundError:
        return []

# Get whisper model
global model
model = None
def load_model():
    global progress_label, transcript_btn, model, root
    if not model:
        # UI update
        progress_label.config(text="⏳ Model loading!")
        transcript_btn.config(state = tk.DISABLED)

        # Load model and count the time
        start = time.time()
        download_root = os.path.join(BASE, "src/resource")
        model = whisper.load_model("large-v3-turbo", download_root=download_root)
        end = time.time()

        args = (start, end)
        root.after(0, on_loaded_model, *args)

def on_loaded_model(start, end):
    # Print out
    progress_label.config(text=f"✅ Model loaded ({round(end - start, 2)}s)!")
    transcript_btn.config(state = tk.ACTIVE)

# Create the main window
def build_ui():
    global root
    root = tk.Tk()
    root.title("Transcriptor")

    # Set style
    style = ttk.Style(root)
    style.theme_use('clam')

    global setup_done_bv, input_path_sv, log_path_sv, log_sv, output_dir_sv, selected_dir_sv, saved_dirs_sv
    setup_done_bv = tk.BooleanVar()
    input_path_sv = tk.StringVar()
    log_path_sv = tk.StringVar()
    log_sv = tk.Variable()
    output_dir_sv = tk.StringVar()
    selected_dir_sv = tk.StringVar()
    saved_dirs_sv = tk.Variable()

    input_path_sv.set("")
    selected_dir_sv.set("Select a save in progress")

    # Get the global vars for UI
    global browse_audio_button, transcript_btn, dropdown
    global progress_bar, progress_label, remaining_time_label, remaining_time_label, mean_speed_label, latency_label
    
    # UI: Audio selection
    tk.Label(root, text="Audio wav file:").grid(row=0, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=input_path_sv, width=50).grid(row=0, column=1, padx=10, pady=10)
    browse_audio_button = tk.Button(root, text="Browse", command=browse_audio)
    browse_audio_button.grid(row=0,column=2,padx=10,pady=10)

    # UI: Saved Directory selection (dropdown)
    tk.Label(root, text="Select a save in progress").grid(row=1, column=0, padx=10, pady=10)
    saved_dirs_sv.set(get_subdirs(TEMP_CONTAINER_DIR))
    dropdown = ttk.Combobox(root, width=40, textvariable=selected_dir_sv, values=saved_dirs_sv.get(), state="readonly")
    dropdown.grid(row=1, column=1, padx=20, pady=20, sticky="w")
    dropdown.bind("<<ComboboxSelected>>", on_dropdown_select)

    # UI: Refresh button (to remove the effect of DISABLED)
    refresh_btn = ttk.Button(root, text="Refresh", command=refresh)
    refresh_btn.grid(row=1, column=2, padx=10, pady=10)

    # UI: Output directory
    tk.Label(root, text="Saved Directory:").grid(row=2, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=output_dir_sv, width=50).grid(row=2, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=browse_directory).grid(row=2, column=2, padx=10, pady=10)

    # UI: Transcript Button
    transcript_btn = tk.Button(root, text="Process audio", command=process_audio)
    transcript_btn.grid(row=3, column=0, columnspan=3, pady=20)

    # UI: Progress Bar and Labels
    progress_label = tk.Label(root, text="")
    progress_label.grid(row=4, column=0, columnspan=3, pady=10)
    progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
    progress_bar.grid(row=5, column=0, columnspan=3, pady=10)

    # UI: Data during the transcription
    remaining_time_label = tk.Label(root, text="")
    remaining_time_label.grid(row=6, column=0, columnspan=1, pady=10, padx=5)
    mean_speed_label = tk.Label(root, text="")
    mean_speed_label.grid(row=6, column=1, columnspan=1, pady=10, padx=5)
    latency_label = tk.Label(root, text="")
    latency_label.grid(row=6, column=2, columnspan=1, pady=10, padx=5)
    
    threading.Thread(target=load_model).start()

def refresh():
    setup_done_bv.set(False)
    input_path_sv.set("")
    log_path_sv.set("")
    log_sv.set(None)
    output_dir_sv.set("")
    selected_dir_sv.set("Select a save in progress")

    browse_audio_button.config(state = tk.ACTIVE)
    dropdown.config(state = tk.ACTIVE)

# Function to browse for CSV file
def browse_audio():
    global dropdown
    filename = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3"), ("WAV files", "*.wav")])
    input_path_sv.set(filename)
    dropdown.config(state = tk.DISABLED)

def on_dropdown_select(event):
    global browse_audio_button
    browse_audio_button.config(state = tk.DISABLED)

# Function to browse for saved directory
def browse_directory():
    global dropdown
    directory = filedialog.askdirectory()
    if directory:
        output_dir_sv.set(directory)
        dropdown.config(state = tk.DISABLED)

# Function to get the output dir
def process_audio():
    global browse_audio_button, dropdown, progress_bar
    global progress_label, remaining_time_label, latency_label, mean_speed_label
    global input_path_sv, selected_dir_sv, log_path_sv, log_sv

    # Only one of the two is chosen
    filename = input_path_sv.get()
    selected_dir = selected_dir_sv.get() # It's shortenned for ease of access

    # If selected_dir, then log_path is not initialized
    if selected_dir:
        selected_dir = os.path.join(TEMP_CONTAINER_DIR, selected_dir_sv.get()) # It's shortenned for ease of access
        selected_dir_sv.set(selected_dir) 
        log_path = os.path.join(selected_dir, "log.json")
    else:
        log_path = log_path_sv.get()
    output_dir = output_dir_sv.get()

    def setup_audio_dir() -> dict:
        global model
        
        # Get current time
        current_time = time.ctime(time.time()).replace(":", "-").replace(" ", "-")

        # Get temp dir and log
        log_path = log_path_sv.get()
        temp_dir = filename.split("/")[-1].split(".")[0] + "-" + current_time
        temp_dir = os.path.join(TEMP_CONTAINER_DIR, temp_dir)
        if not log_path:
            log_path = os.path.join(temp_dir, "log.json")
            log_path_sv.set(log_path)

        # Create directory in temp
        os.makedirs(temp_dir, exist_ok = True)    
            
        # Check for log
        log = {
            "temp_dir": temp_dir,
            "main_wav_path": os.path.join(temp_dir, "main.wav"),
            "log_path": log_path,
            "main_duration_s": None,
            "interval_s": 30, # TODO: add a function to allow customizing it
            "chunked": False,
            "chunk_path": [],
            "progress": 0
        }
        if not os.path.exists(log_path):
            with open(log_path, "x", encoding="utf-8") as file:
                json.dump(log, file)
        else:
            try:
                with open(log_path, 'r', encoding="utf-8") as file:
                    log = json.load(file)
                print("Data loaded successfully:", log)
            except FileNotFoundError as e:
                raise Exception(e)
            except json.JSONDecodeError as e:
                with open(log_path, "w", encoding="utf-8") as file:
                    json.dump(log, file)
            
        # Convert or save file main.wav if necessary
        if filename.endswith(".mp3"):
            print(log)
            mp3_to_wav(filename, wav_path = log["main_wav_path"])
        elif filename.endswith(".wav"):
            try:
                shutil.copyfile(filename, dst = log["main_wav_path"])
                print(f"File copied from {filename} to {log['main_wav_path']} successfully.")
            except FileNotFoundError:
                print(f"Error: Source file '{filename}' not found.")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            raise Exception("Wrong type of file!")
        
        if not log["chunked"]:
            audio = AudioSegment.from_wav(log["main_wav_path"])
            duration_ms = len(audio)

            if duration_ms > 30 * 1000:
                chunk_files = chunk_wav_to_files(log["main_wav_path"], output_dir=temp_dir, chunk_seconds=30)
                log["chunk_path"] = chunk_files
            else:
                log["chunk_path"] = [log["main_wav_path"]]

            log["chunked"] = True
            log["main_duration_s"] = duration_ms / 1000
            with open(log_path, "w", encoding="utf-8") as file:
                json.dump(log, file)
        
        # Finalize setup
        _ = list(saved_dirs_sv.get())
        _.append(temp_dir)
        saved_dirs_sv.set(_)
        setup_done_bv.set(True)
        log_sv.set(log)

        # Return log as result of setup
        return log
    
    # Prioritize saved file over audio file
    setup_done = setup_done_bv.get()
    if filename and not setup_done:
        log = setup_audio_dir()
    elif filename:
        with open(log_path, "r") as file:
            log = json.load(file)
        messagebox.showerror("Error", "Log is not available. Check the save file.")
        return
    elif selected_dir:
        with open(log_path, "r") as file:
            log = json.load(file)
    else:
        messagebox.showerror("Error", f"Something is wrong with log file.")
        return

    # Show progress bar and download status
    progress_bar['maximum'] = len(log["chunk_path"])
    progress_label['text'] = f"Transcripting 0/{len(log['chunk_path'])} audio files..."
    remaining_time_label['text'] = "Remaining time: estimating..."
    mean_speed_label['text'] = "Mean speed: 0 chunk/s"
    latency_label['text'] = "Mean latency: 0 s/chunk"

    def transcript():
        total_size = 0
        total_time = 0
        start_time = time.time()

        starting_num = log["progress"]
        for i, audio_file in enumerate(log["chunk_path"][starting_num:], start=starting_num):
            try:
                transcript_start_time = time.time()
                result = model.transcribe(audio_file)
                elapsed_time = time.time() - transcript_start_time

                # Update total size and time for mean speed calculation
                total_size += 1 # 1 chunk
                total_time += elapsed_time

                # Calculate mean speed in Mbit/s
                mean_speed = total_size / total_time if total_time > 0 else 0
                mean_speed_label['text'] = f"Mean speed  : {mean_speed:.2f} chunk/s ({log['interval_s']}s per chunk)"
                latency_label['text']    = f"Mean latency: {1/mean_speed:.2f} s/chunk"

                # Get chunk start time and end time
                chunk_start = int(log["progress"] * log["interval_s"])

                # Process to get the minutes and seconds
                chunk_start_min = int(chunk_start / 60) # To floor
                chunk_start_s = int(chunk_start - chunk_start_min * 60)
                
                # Get the time interval and concate string
                time_interval_str = f"# [{chunk_start_min}:{chunk_start_s:02d}] - "
                output = time_interval_str + result["text"] + "\n\n"

                # Get output path
                output_txt_path = f"out.txt"
                if output_dir:
                    temp_output = os.path.join(log["temp_dir"], output_txt_path)
                    output_txt_path = os.path.join(output_dir, output_txt_path)
                else:
                    temp_output = output_txt_path = os.path.join(log["temp_dir"], output_txt_path)

                # Check if there exists an ongoing progress
                if os.path.exists(temp_output):
                    with open(temp_output, "r", encoding="utf-8") as fr:
                        output = fr.read() + output
                
                # Write into output file
                try:
                    with open(temp_output, 'x', encoding="utf-8") as handler:
                        handler.write(output)
                except Exception as e:
                    with open(temp_output, 'w', encoding="utf-8") as handler:
                        handler.write(output)
                try:
                    with open(output_txt_path, 'x', encoding="utf-8") as handler:
                        handler.write(output)
                except Exception as e:
                    with open(output_txt_path, 'w', encoding="utf-8") as handler:
                        handler.write(output)
                
                # If there is an output dir, send them there too
                if output_dir:
                    shutil.copyfile(temp_output, output_txt_path)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to transcript {audio_file}: {e}")

            # Update progress
            log["progress"] = log["progress"] + 1
            with open(log["log_path"], "w", encoding="utf-8") as file:
                json.dump(log, file)
            
            # Estimate remaining time
            current_time = time.time()
            elapsed_total_time = current_time - start_time
            args = (log, elapsed_total_time, i, starting_num)
            root.after(0, update_progress, *args)

        # Inform the user of completion
        messagebox.showinfo("Success", "Audio files have been processed successfully.")
        progress_bar['value'] = 0
        progress_label['text'] = ""
        remaining_time_label['text'] = ""
        mean_speed_label['text'] = ""
        latency_label['text'] = ""

    # Run the process function in a separate thread
    threading.Thread(target=transcript).start()

def update_progress(log, elapsed_total_time, i, starting_num):
    progress_bar['value'] = log["progress"]
    progress_label['text'] = f"Transcripting {log['progress']}/{len(log['chunk_path'])} audio files..."

    if i - starting_num + 1 > 0:
        avg_time_per_audio = elapsed_total_time / (i - starting_num + 1)
        remaining_time = avg_time_per_audio * (len(log["chunk_path"]) - (i - starting_num + 1))
        remaining_time_label['text'] = f"Remaining time: {remaining_time:.2f}s"
    else:
        remaining_time_label['text'] = "Remaining time: estimating..."

if __name__ == "__main__":
    # Initialization
    global root
    os.makedirs(TEMP_CONTAINER_DIR, exist_ok=True)
    build_ui()

    # Main loop
    root.mainloop()