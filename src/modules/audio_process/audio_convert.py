import librosa
import soundfile as sf

def mp3_to_wav(mp3_path, wav_path):
    """
    Converts an MP3 file to WAV format.

    Args:
      mp3_path: Path to the input MP3 file.
      wav_path: Path to save the output WAV file.
    """
    try:
      y, sr = librosa.load(mp3_path)
      sf.write(wav_path, y, sr)
      print(f"Successfully converted {mp3_path} to {wav_path}")
    except Exception as e:
      print(f"Error during conversion: {e}")

if __name__ == "__main__":
    # Example usage:
    mp3_file = "audio.mp3"  # Replace with your MP3 file path
    wav_file = "audio.wav" # Replace with your desired WAV file path

    mp3_to_wav(mp3_file, wav_file)