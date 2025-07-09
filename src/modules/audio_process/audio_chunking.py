import os
from pydub import AudioSegment

def chunk_wav_to_files(input_path: str, output_dir: str, chunk_seconds: int = 5):
    audio = AudioSegment.from_wav(input_path)
    duration_ms = len(audio)
    chunk_ms = chunk_seconds * 1000

    os.makedirs(output_dir, exist_ok=True)

    num_chunks = (duration_ms + chunk_ms - 1) // chunk_ms # round up

    for i in range(num_chunks):
        # Process and export to files in output directory
        start_ms = i * chunk_ms
        end_ms = min(start_ms + chunk_ms, duration_ms)
        audio_chunk = audio[start_ms:end_ms]
        out_path = os.path.join(output_dir, f"chunk_{i:04d}.wav")
        audio_chunk.export(out_path, format="wav")
        
        # Process audio chunks directly
        # result = engine.process_audio(audio_chunk, is_last=False)

        # Print out the results
        print(f"({(end_ms - start_ms)/1000:.2f}s)")
        print("\n\n=================================\n\n")

if __name__ == "__main__":
    chunk_wav_to_files("audio.wav", "output_chunks", chunk_seconds=5)