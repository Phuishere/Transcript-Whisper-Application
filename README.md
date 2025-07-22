# Transcript-Application
- A transcript application using Tkinter interface with a Whisper backend.
- Removed the use of ViStreamASR due to unsolved memory leakage on Window and quality issue (perhaps due to the improper way of processing signal data).
- The setting up is straight forward: ```pip install -r requirements.txt```
- To package the file (icon is from ChatGPT):
```
pyinstaller --add-data "src/resource;src/resource" --add-data "src/temp;src/temp" --icon="src/resource/icon.ico" --noconfirm --onefile --windowed src/main.py
```