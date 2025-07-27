# Transcript-Application
- A transcript application using Tkinter interface with a Whisper backend.
- Removed the use of ViStreamASR due to unsolved memory leakage on Window and quality issue (perhaps due to the improper way of processing signal data).
- The setting up is straight forward: ```pip install -r requirements.txt```
- To package the file (icon is from ChatGPT):
```
pyinstaller --hidden-import pydub --hidden-import librosa --add-data "src/resource;src/resource" --add-data "src/modules;modules" --add-data "src\resource\temp;src\resource\temp" --icon="src/resource/icon.ico" --noconfirm --onedir --noconsole --windowed src/main.py
```
- Include Whisper library if necessary:
```
--add-data "venv\Lib\site-packages\whisper;whisper"
```
- Include chocolatey in ```src/resource``` to have it in the bundled folder of pyinstaller
- Run this ?
```
--exclude-module pyinstaller
```