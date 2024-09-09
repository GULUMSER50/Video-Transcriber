import logging
from openai import OpenAI
from config import OPENAI_API_KEY, WHISPER_MODEL
from pydub import AudioSegment
import os

client = OpenAI(api_key=OPENAI_API_KEY)

logger = logging.getLogger(__name__)

def split_audio(audio_file_path, chunk_length_ms=60000):
    audio = AudioSegment.from_wav(audio_file_path)
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i+chunk_length_ms]
        chunk_path = f"{audio_file_path}_chunk_{i//chunk_length_ms}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
    return chunks

def transcribe_audio(audio_file_path):
    try:
        logger.info(f"Attempting to transcribe audio file: {audio_file_path}")
        logger.info(f"Using Whisper model: {WHISPER_MODEL}")
        
        # Split audio into chunks
        chunks = split_audio(audio_file_path)
        
        full_transcript = ""
        for chunk in chunks:
            with open(chunk, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model=WHISPER_MODEL,
                    file=audio_file
                )
            full_transcript += transcript.text + " "
            os.remove(chunk)  # Remove the temporary chunk file
        
        logger.info("Transcription successful")
        return full_transcript.strip(), "en"  # Assuming English for now, you may need to detect language
    except Exception as e:
        logger.exception(f"Error in transcription: {str(e)}")
        return None, None