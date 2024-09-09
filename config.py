import os
import json
from pathlib import Path

# Get the current working directory
CURRENT_DIR = Path(__file__).parent.absolute()

# Path to the config file
CONFIG_FILE = CURRENT_DIR / 'secure_config.json'

def get_api_key():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('OPENAI_API_KEY')
    return None

def set_api_key(api_key):
    config = {'OPENAI_API_KEY': api_key}
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

# OpenAI API key
OPENAI_API_KEY = get_api_key()

if not OPENAI_API_KEY:
    new_key = input("Enter your OpenAI API Key: ")
    set_api_key(new_key)
    OPENAI_API_KEY = new_key

# Supported languages
LANGUAGES = [
    "English", "Spanish", "French", "German", "Italian", "Portuguese", "Dutch", 
    "Russian", "Chinese", "Japanese", "Korean", "Arabic", "Hindi", "Bengali", 
    "Turkish", "Vietnamese", "Thai", "Indonesian", "Malay", "Swahili"
]

# Whisper model name
WHISPER_MODEL = "whisper-1"

# OpenAI model for translation (changed to a less expensive model)
TRANSLATION_MODEL = "gpt-3.5-turbo-16k"

# Temporary file names with full paths
TEMP_VIDEO = os.path.join(CURRENT_DIR, "temp_video.mp4")
TEMP_AUDIO = os.path.join(CURRENT_DIR, "temp_audio.wav")