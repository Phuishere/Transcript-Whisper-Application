# Get path in src/
import sys
sys.path.insert(0, "src")
sys.stdout.reconfigure(encoding="utf-8")

# Code
import time
import os
from libs.ViStreamASR import StreamingASR
print(f"Imports successful")

# Initialize StreamingASR
asr = StreamingASR(chunk_size_ms=640, debug=False)
print(f"StreamingASR initialized (chunk_size: {asr.chunk_size_ms}ms)")

# Test with audio file
audio_file = "src/resource/audio.wav"
if not os.path.exists(audio_file):
    print(f"Audio file not found: {audio_file}")

print(f"Testing with audio file: {audio_file}")

# Process audio
start_time = time.time()
partial_count = 0
final_count = 0
final_segments = []

print(f"\nProcessing audio...")
for result in asr.stream_from_file(audio_file):
    if result.get('partial'):
        partial_count += 1
        if partial_count <= 3:  # Show first few partials
            text = result['text'][:60] + "..." if len(result['text']) > 60 else result['text']
            print(f"   Partial {partial_count}: {text}")
    
    if result.get('final'):
        final_count += 1
        final_text = result['text']
        final_segments.append(final_text)
        print(f"Final {final_count}: {final_text}")

end_time = time.time()
processing_time = end_time - start_time

# Results
print(f"\nTest Results:")
print(f"   - Processing time: {processing_time:.2f} seconds")
print(f"   - Partial updates: {partial_count}")
print(f"   - Final segments: {final_count}")
print(f"   - Complete transcription:")

complete_text = " ".join(final_segments)
print(f"     {complete_text}")

print(f"\nTest completed successfully!")