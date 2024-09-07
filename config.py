import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Supported languages
LANGUAGES = [
    "English", "Spanish", "French", "German", "Italian", "Portuguese", "Dutch", 
    "Russian", "Chinese", "Japanese", "Korean", "Arabic", "Hindi", "Bengali", 
    "Turkish", "Vietnamese", "Thai", "Indonesian", "Malay", "Swahili"
]

# Whisper model name
WHISPER_MODEL = "base"

# OpenAI model for translation
TRANSLATION_MODEL = "gpt-3.5-turbo"

# Temporary file names
TEMP_VIDEO = "temp_video.mp4"
TEMP_AUDIO = "temp_audio.wav"