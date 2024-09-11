import os
import json
from pathlib import Path

# Get the current working directory
CURRENT_DIR = Path(__file__).parent.absolute()

# Path to the config file
CONFIG_FILE = CURRENT_DIR / 'secure_config.json'

# Define input and output directories
INPUT_DIR = CURRENT_DIR / 'data' / 'input'
OUTPUT_DIR = CURRENT_DIR / 'data' / 'output'

# Add this near the top of the file, with other imports
from pathlib import Path

# Add this with other path definitions
TEMP_AUDIO = OUTPUT_DIR / "temp_audio.wav"

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

# Ensure input and output directories exist
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Temporary file names with full paths
TEMP_VIDEO = OUTPUT_DIR / "temp_video.mp4"
TEMP_AUDIO = OUTPUT_DIR / "temp_audio.wav"

# Function to get a valid input file path
def get_input_file_path(filename):
    return INPUT_DIR / filename

# Function to get a valid output file path
def get_output_file_path(filename, extension='.srt'):
    # Remove any existing extension from the filename
    base_name = Path(filename).stem
    # Create the new filename with the specified extension
    new_filename = f"{base_name}{extension}"
    return OUTPUT_DIR / new_filename

# Function to get a transcript file path
def get_transcript_file_path(video_filename, timestamp):
    base_name = f"{Path(video_filename).stem}_{timestamp}_transcript"
    return get_output_file_path(base_name, extension='.srt')

# Update the debug function to remove .txt file checks
def debug_file_paths(video_filename, timestamp):
    input_file = get_input_file_path(video_filename)
    srt_file = get_transcript_file_path(video_filename, timestamp)
    
    print(f"Input file path: {input_file}")
    print(f"Input file exists: {input_file.exists()}")
    print(f"SRT file path: {srt_file}")
    print(f"SRT file exists: {srt_file.exists()}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in input directory: {list(INPUT_DIR.glob('*'))}")
    print(f"Files in output directory: {list(OUTPUT_DIR.glob('*'))}")