# Transcript-Application
- A transcript application using Tkinter interface with a Whisper backend.
- Removed the use of ViStreamASR due to unsolved memory leakage on Window and quality issue (perhaps due to the improper way of processing signal data).
- The setting up is straight forward: ```pip install -r requirements.txt```
- To package the file (icon is from ChatGPT):
```
pyinstaller --hidden-import pydub --hidden-import librosa --add-data "src/resource;src/resource" --add-data "src/temp;src/temp" --add-binary "src/ffmpeg/ffmpeg.exe;src/ffmpeg/ffmpeg.exe" --add-binary "src/ffmpeg/ffprobe.exe;src/ffmpeg/ffprobe.exe" --icon="src/resource/icon.ico" --noconfirm --onedir --noconsole --windowed src/main.py
```
- Get file ffmpeg.exe and ffprobe.exe and put it into src/ffmpeg.
- Run this ?
```
--exclude-module pyinstaller
```