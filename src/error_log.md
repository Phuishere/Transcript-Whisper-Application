# Error log during dev

## Error [WinError 32]
### Description:
- When using the sample code, things break.
```
from ViStreamASR import StreamingASR

# Initialize ASR
asr = StreamingASR()

# Process audio file
for result in asr.stream_from_file("audio.mp3"):
    if result['partial']:
        print(f"Partial: {result['text']}")
    if result['final']:
        print(f"Final: {result['text']}")
```
- Reason: WinError 32 with file .pt still opened. This seems to only happen in Windows
- Log:
```
PermissionError: [WinError 32] The process cannot access the file because it is being used by another process: 'C:\\Users\\ADMIN\\AppData\\Local\\Temp\\tmpj6m6vzlh.pt'
```
### Solution:
- Fix the source code of ViStreamASR by moving this below one indent
```
# From
with tempfile.NamedTemporaryFile(suffix='.pt', delete=False) as temp_model:
    ...
    os.unlink(temp_model.name)

# To
with tempfile.NamedTemporaryFile(suffix='.pt', delete=False) as temp_model:
    ...
os.unlink(temp_model.name)
```

## Encoding error when flushing into files (utf-8 error with Vietnamese characters)
### Description:
- UTF-8 not working when flushing
- Log:
```
UnicodeEncodeError: 'charmap' codec can't encode character '\u01b0' in position 2: character maps to <undefined>
```
### Solution:
- Adding ```encoding="utf-8"``` in the tempfile opening
- E.g. ```temp_lexicon = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding="utf-8")```

## OS error with no space left
### Description:
- Error when initializing models (core.ASREngine.initialize_models)
- Usually when the Disk space is not available
- Log: ```OSError: [Errno 28] No space left on device```
### Solution:
- Free the disk space

## Memory leakage issue
### Description:
- Memory is taken up when running the model (up to 10GB!). Some increases are still there after the program stops
- This could be because of:
    + Inherent tempfile mismanagement: during the loading of model - lm_file in core.py (ViStreamASR)
    + My own fixes
### Solutions: