import speech_recognition as sr
from pydub import AudioSegment
import os
from ..utils.helpers import ensure_dir

def transcribe_audio(audio_path):
    # Convert audio to WAV format using pydub
    audio = AudioSegment.from_file(audio_path)
    wav_path = audio_path.rsplit('.', 1)[0] + '.wav'
    audio.export(wav_path, format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio, show_all=True)
        if isinstance(text, dict) and 'alternative' in text:
            transcript = text['alternative'][0]['transcript']
            detected_lang = text['language'] if 'language' in text else 'unknown'
        else:
            print(f"Unexpected transcription result: {text}")
            transcript = str(text)  # Convert to string if it's not already
            detected_lang = 'unknown'
        
        # Clean up temporary WAV file
        os.remove(wav_path)
        
        return transcript, detected_lang
    except sr.UnknownValueError:
        print("Speech Recognition could not understand the audio")
        return "Speech Recognition could not understand the audio", None
    except sr.RequestError as e:
        print(f"Could not request results from Speech Recognition service; {e}")
        return f"Could not request results from Speech Recognition service; {e}", None
    except Exception as e:
        print(f"An unexpected error occurred during transcription: {e}")
        return f"An unexpected error occurred during transcription: {e}", None
    finally:
        # Ensure temporary WAV file is removed even if an exception occurs
        if os.path.exists(wav_path):
            os.remove(wav_path)