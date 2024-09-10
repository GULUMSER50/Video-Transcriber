import os
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

# Get OpenAI API key from environment variable
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables")

# List of supported languages
LANGUAGES = [
    "English", "Spanish", "French", "German", "Italian", "Portuguese", "Dutch", 
    "Russian", "Chinese", "Japanese", "Korean", "Arabic", "Hindi", "Bengali", 
    "Turkish", "Vietnamese", "Thai", "Indonesian", "Malay", "Swahili"
]