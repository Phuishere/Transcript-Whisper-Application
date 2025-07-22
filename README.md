# Transcript-Application
- A transcript application using Tkinter interface with a Whisper backend.
- Removed the use of ViStreamASR due to unsolved memory leakage on Window and quality issue (perhaps due to the improper way of processing signal data).
- The setting up is straight forward: ```pip install -r requirements.txt```