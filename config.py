import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the current working directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

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

# OpenAI model for translation (changed to a less expensive model)
TRANSLATION_MODEL = "gpt-3.5-turbo-16k"

# Temporary file names with full paths
TEMP_VIDEO = os.path.join(CURRENT_DIR, "temp_video.mp4")
TEMP_AUDIO = os.path.join(CURRENT_DIR, "temp_audio.wav")