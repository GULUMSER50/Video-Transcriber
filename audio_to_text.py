import whisper
from config import WHISPER_MODEL

def transcribe_audio(audio_file):
    print(f"Starting transcription of {audio_file}")
    model = whisper.load_model(WHISPER_MODEL)
    
    result = model.transcribe(audio_file)
    
    print(f"Transcription completed. Detected language: {result['language']}")
    return result["text"], result["language"]
