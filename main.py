import streamlit as st
import os
import logging
import time
from openai import OpenAIError
from config import (
    get_input_file_path,
    get_transcript_file_path,
    debug_file_paths,
    INPUT_DIR,
    OUTPUT_DIR,
    LANGUAGES,
    TEMP_AUDIO
)
from src.video.video_to_audio import extract_audio as convert_video_to_audio
from src.audio.audio_to_text import transcribe_audio, TranscriptionError
from src.text_translation import translate_text
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Video Transcriber & Translator", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    body {
        font-family: 'Inter', Arial, sans-serif;
    }
    .stApp {
        background: linear-gradient(rgba(5, 25, 55, 0.95), rgba(0, 77, 122, 0.95));
    }
    .main {
        color: #FFFFFF;
    }
    .title {
        color: #FFFFFF;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        padding: 1rem 0;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #E0E0E0;
        font-size: 1.25rem;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .author {
        color: #CCCCCC;
        font-size: 0.9rem;
        font-style: italic;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        text-transform: uppercase;
    }
    .stTextInput > div > div > input,
    .stSelectbox > div,
    .stMultiSelect > div {
        background-color: rgba(255, 255, 255, 0.1);
        color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    a {
        color: #3498db;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    .stFileUploader > button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    .stFileUploader > button:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
    }
    .stFileUploader > div[data-testid="stFileUploadDropzone"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px dashed rgba(255, 255, 255, 0.2) !important;
    }
    .upload-video-text, .select-languages-text {
        color: #FFFFFF;
        margin-bottom: 0.5rem;
    }
    .app-description {
        position: fixed;
        left: 10px;
        bottom: 10px;
        font-size: 0.8em;
        color: rgba(255,255,255,0.7);
        background-color: rgba(0,0,0,0.3);
        padding: 5px 10px;
        border-radius: 5px;
        max-width: 60%;
    }
    .fancy-separator {
        border: 0;
        height: 1px;
        background-image: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0));
        margin: 20px 0;
    }
    .white-header {
        color: #FFFFFF;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .download-button {
        background-color: #3498db;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        font-weight: bold;
        margin-top: 10px;
        display: inline-block;
    }
    .download-button:hover {
        background-color: #2980b9;
    }
    .download-explanation {
        color: #CCCCCC;
        font-size: 0.9rem;
        margin-top: 5px;
    }
    /* Remove all spacing around the video */
    .stVideo {
        margin-bottom: 0 !important;
    }
    .stVideo > div {
        margin: 10 !important;
        padding: 10 !important;
        
    }
    .stDownloadButton>button {
        background-color: #3498db;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: none;
        font-weight: bold;
        margin-top: 10px;
        text-transform: none;
    }
    .stDownloadButton>button:hover {
        background-color: #2980b9;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='title'>Video Transcriber & Translator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Convert, Transcribe, and Translate with Ease!</p>", unsafe_allow_html=True)
st.markdown("<p class='author'>by <a href='https://www.linkedin.com/in/g%C3%BCl%C3%BCmser-eskiturk-86687b150/' target='_blank' style='color: #CCCCCC; text-decoration: none;'>Gülümser Eskitürk</a></p>", unsafe_allow_html=True)

# Create two columns for inputs
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<h3 class='upload-video-text'>Upload Your Video</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload video file", type=["mp4", "avi", "mov", "mkv", "flv", "wmv", "webm"], label_visibility="collapsed")

with col2:
    st.markdown("<h3 class='select-languages-text'>Select Languages</h3>", unsafe_allow_html=True)
    selected_languages = st.multiselect("Select target languages", LANGUAGES, label_visibility="collapsed")

# Define the data directory
DATA_DIR = Path(os.path.expanduser("~/Desktop/grad_project_upschool/Video-Transcriber/data"))

# Ensure the data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

def process_video(uploaded_file, selected_languages):
    # Generate a unique filename for the uploaded video
    video_filename = f"{uploaded_file.name}_{int(time.time())}"
    video_path = DATA_DIR / video_filename

    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    col1, col2, col3 = st.columns(3)
    
    with col1:
        progress_bar = st.progress(0)
    
    with col2:
        status_text = st.empty()
    
    with col3:
        info_text = st.empty()
    
    with st.spinner("Processing video..."):
        try:
            # Video to Audio
            status_text.text("Converting video to audio...")
            progress_bar.progress(25)
            audio_file = convert_video_to_audio(str(video_path), TEMP_AUDIO)
            
            if audio_file:
                # Transcription
                status_text.text("Transcribing audio...")
                progress_bar.progress(50)
                try:
                    transcript, detected_lang = transcribe_audio(audio_file)
                    if not transcript:
                        raise TranscriptionError("Empty transcript returned")
                except TranscriptionError as e:
                    st.error(f"Transcription failed: {str(e)}")
                    logger.error(f"Transcription failed: {str(e)}")
                    return

                if transcript:
                    progress_bar.progress(75)
                    info_text.success("Transcription completed successfully")
                    st.markdown("<h2 class='white-header'>Transcription and Translation Results</h2>", unsafe_allow_html=True)
                    st.markdown("<hr class='fancy-separator'>", unsafe_allow_html=True)
                    # Convert language code to full name
                    full_lang_name = next((lang for lang in LANGUAGES if lang.lower().startswith(detected_lang.lower())), detected_lang)
                    st.markdown(f"<h4 style='color: white;'>Detected language: {full_lang_name}</h3>", unsafe_allow_html=True)
                    
                    # Add download button for original transcript
                    srt_content = f"1\n00:00:00,000 --> 00:00:05,000\n{transcript}"
                    st.download_button(
                        label=f"Download {full_lang_name} transcript",
                        data=srt_content,
                        file_name=f"original_transcript_{full_lang_name}.srt",
                        mime="text/srt",
                        key="download_original",
                    )
                    
                    st.markdown("<hr class='fancy-separator'>", unsafe_allow_html=True)
                    
                    # Save transcripts and translations


                    transcript_file = get_transcript_file_path(video_filename, int(time.time()))
                    with open(transcript_file, 'w', encoding='utf-8') as f:


                        f.write(transcript)

                    # Translation
                    for lang in selected_languages:
                        if lang.lower() != full_lang_name.lower():
                            try:
                                status_text.text(f"Translating to {lang}...")
                                translated_text = translate_text(transcript, lang)
                                if translated_text:
                        
                        
                                    st.markdown(f"<h4 style='color: white;'>Translation to {lang}</h4>", unsafe_allow_html=True)
                                    
                                    # Prepare SRT content
                                    srt_content = f"1\n00:00:00,000 --> 00:00:05,000\n{translated_text}"
                                    
                                    download_button = st.download_button(
                                        label=f"Download {lang} translation",
                                        data=srt_content,
                                        file_name=f"translation_{lang}.srt",
                                        mime="text/srt",
                                        key=f"download_{lang}",
                                    )
                                    
                                    st.markdown("<hr class='fancy-separator'>", unsafe_allow_html=True)
                                    # Save translations
                                    output_dir = DATA_DIR / "output"
                                    output_dir.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists
                                    translation_path = output_dir / f"{video_filename}_translation_{lang}.srt"
                                    with open(translation_path, "w", encoding='utf-8') as f:
                                        f.write(srt_content)
                                else:
                                    st.warning(f"Translation to {lang} failed.")
                            except OpenAIError as e:
                                st.error(f"An error occurred during translation to {lang}: {str(e)}")
                        else:
                            st.markdown(f"<h4 style='color: white;'>Skipping translation to {lang} as it's the detected original language.</h4>", unsafe_allow_html=True)
                    
                    progress_bar.progress(100)
                    status_text.text("Processing complete!")
                    info_text.success("All tasks completed successfully!")
                else:
                    st.error("Transcription failed: Empty transcript returned.")
                    logger.error("Transcription failed: Empty transcript returned")
            else:
                st.error("Failed to convert video to audio. The video file may be corrupted, in an unsupported format, or may not contain an audio track.")
                logger.error("Failed to convert video to audio")
        except Exception as e:
            st.error(f"An error occurred during processing: {str(e)}")
            logger.exception("Error during processing")
        
        # Clean up temporary files
        for temp_file in [video_path, TEMP_AUDIO]:
            if os.path.exists(temp_file):
                os.remove(temp_file)

        # Remove temporary SRT files
        for file in output_dir.glob(f"{video_filename}_translation_*.srt"):
            file.unlink()

# Processing section
if uploaded_file is not None and selected_languages:
    process_video(uploaded_file, selected_languages)

# Add the application description at the bottom left
st.markdown("<div class='app-description'>This application converts video files to audio, creates transcripts, and translates to selected languages.</div>", unsafe_allow_html=True)

# FFmpeg info at the bottom right
st.markdown("<div style='position: fixed; right: 10px; bottom: 10px; font-size: 0.8em; color: rgba(255,255,255,0.5);'>FFmpeg (c) 2000-2024</div>", unsafe_allow_html=True)