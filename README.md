# Video Transcriber and Translator

This Streamlit application converts video files to audio, creates transcripts, and translates them to selected languages using OpenAI's GPT model.

## Features

- Video to audio conversion
- Audio transcription
- Multi-language translation
- Streamlit-based user interface

## Requirements

- Python 3.8+
- FFmpeg (must be installed separately)
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/GULUMSER50/Video-Transcriber.git
   cd Video-Transcriber
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Install FFmpeg:
   - On macOS: `brew install ffmpeg`
   - On Ubuntu: `sudo apt-get install ffmpeg`
   - On Windows: Download from [FFmpeg official website](https://ffmpeg.org/download.html)

4. Set up your OpenAI API key:
   Create a `.env` file in the project root and add your API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the Streamlit app:
```
streamlit run main.py
```

