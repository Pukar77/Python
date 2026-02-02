import whisper
import os
import numpy as np
from pydub import AudioSegment
import tempfile


class WhisperTranscriber:
    """
    Audio to text converter using OpenAI's Whisper model.
    """
    
    def __init__(self, model_size: str = "base"):
        """
        Initialize the Whisper model.
        """
        print(f"Loading Whisper model: {model_size}")
        self.model = whisper.load_model(model_size)
        print("Model loaded successfully!")
    
    def _preprocess_audio(self, audio_path: str) -> str:
        """
        Convert audio to proper WAV format that Whisper can handle.
        Returns path to processed audio file.
        """
        print(f"Pre-processing audio: {audio_path}")
        
        # Load audio with pydub
        audio = AudioSegment.from_file(audio_path)
        
        # Convert to mono, 16kHz, 16-bit (Whisper's required format)
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        audio = audio.set_sample_width(2)  # 16-bit
        
        # Save to temporary file
        temp_path = os.path.join(tempfile.gettempdir(), "whisper_temp.wav")
        audio.export(temp_path, format="wav")
        
        print(f"Audio preprocessed: {temp_path}")
        return temp_path
    
    def _load_audio_as_numpy(self, audio_path: str) -> np.ndarray:
        """
        Load audio file and convert to numpy array.
        """
        # Load with pydub
        audio = AudioSegment.from_file(audio_path)
        
        # Convert to mono, 16kHz
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        
        # Convert to numpy array
        samples = np.array(audio.get_array_of_samples())
        
        # Normalize to float32 in range [-1, 1]
        samples = samples.astype(np.float32) / 32768.0
        
        return samples
    
    def transcribe(
        self, 
        audio_path: str, 
        language: str = None,
        task: str = "transcribe"
    ) -> dict:
        """
        Transcribe audio file to text.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        audio_path = os.path.abspath(audio_path)
        print(f"Processing: {audio_path}")
        
        try:
            # Method 1: Try loading as numpy array directly
            print("Loading audio as numpy array...")
            audio_data = self._load_audio_as_numpy(audio_path)
            
            result = self.model.transcribe(
                audio_data,
                language=language,
                task=task,
                verbose=False,
                fp16=False
            )
        except Exception as e:
            print(f"Method 1 failed: {e}")
            print("Trying alternative method...")
            
            # Method 2: Preprocess and save to temp file
            temp_path = self._preprocess_audio(audio_path)
            
            result = self.model.transcribe(
                temp_path,
                language=language,
                task=task,
                verbose=False,
                fp16=False
            )
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
        return {
            "text": result["text"],
            "language": result.get("language", "unknown"),
            "segments": result.get("segments", [])
        }
    
    def transcribe_with_timestamps(self, audio_path: str) -> list:
        """
        Transcribe with timestamps.
        """
        audio_path = os.path.abspath(audio_path)
        audio_data = self._load_audio_as_numpy(audio_path)
        
        result = self.model.transcribe(
            audio_data, 
            word_timestamps=True, 
            fp16=False
        )
        
        segments = []
        for segment in result["segments"]:
            segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            })
        
        return segments


# Usage
if __name__ == "__main__":
    # Check if pydub can read the file
    audio_file = "catch.wav"
    
    if not os.path.exists(audio_file):
        print(f"Error: File '{audio_file}' not found!")
        print(f"Current directory: {os.getcwd()}")
        exit(1)
    
    # Test pydub first
    print("Testing audio file with pydub...")
    try:
        audio = AudioSegment.from_file(audio_file)
        print(f"  Duration: {len(audio)/1000:.2f} seconds")
        print(f"  Channels: {audio.channels}")
        print(f"  Sample Rate: {audio.frame_rate}")
        print("  Audio file is valid!")
    except Exception as e:
        print(f"  Error reading audio: {e}")
        exit(1)
    
    # Initialize and transcribe
    print("\n" + "="*50)
    transcriber = WhisperTranscriber(model_size="base")
    
    print("\nTranscribing...")
    result = transcriber.transcribe(audio_file)
    
    print(f"\nDetected Language: {result['language']}")
    print(f"\nTranscription:\n{result['text']}")
    with open("Subtitle.txt", "w", encoding="utf-8") as f:
        f.write(result['text'])
    
    # With timestamps
    print("\n" + "="*50)
    print("Timestamped Segments:")
    print("="*50)
    segments = transcriber.transcribe_with_timestamps(audio_file)
    for seg in segments:
        print(f"[{seg['start']:.2f}s - {seg['end']:.2f}s]: {seg['text']}")
