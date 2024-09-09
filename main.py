import streamlit as st
import os
import time
from openai import OpenAIError
from config import LANGUAGES, TEMP_VIDEO, TEMP_AUDIO
from src.video.video_to_audio import extract_audio as convert_video_to_audio
from src.audio.audio_to_text import transcribe_audio
from src.text_translation import translate_text

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
    .stFileUploader > div {
        background-color: rgba(255, 255, 255, 0.1);
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
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='title'>Video Transcriber & Translator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Convert, Transcribe, and Translate with Ease</p>", unsafe_allow_html=True)
st.markdown("<p class='author'>by <a href='https://www.linkedin.com/in/g%C3%BCl%C3%BCmser-eskiturk-86687b150/' target='_blank' style='color: #CCCCCC; text-decoration: none;'>Gülümser Eskitürk</a></p>", unsafe_allow_html=True)

# Create two columns for inputs
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<h3 class='upload-video-text'>Upload Your Video</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["mp4", "avi", "mov"])

with col2:
    st.markdown("<h3 class='select-languages-text'>Select Languages</h3>", unsafe_allow_html=True)
    selected_languages = st.multiselect("", LANGUAGES)

# Display uploaded video
if uploaded_file:
    st.video(uploaded_file, start_time=0)

# Processing section
if uploaded_file is not None and selected_languages:
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.spinner("Processing video..."):
        with open(TEMP_VIDEO, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Video to Audio
        status_text.text("Converting video to audio...")
        progress_bar.progress(25)
        audio_file = convert_video_to_audio(TEMP_VIDEO, TEMP_AUDIO)
        
        if audio_file:
            try:
                # Transcription
                status_text.text("Transcribing audio...")
                progress_bar.progress(50)
                start_time = time.time()
                transcript, detected_lang = transcribe_audio(audio_file)
                end_time = time.time()
                
                if transcript:
                    progress_bar.progress(75)
                    st.success(f"Transcription completed in {end_time - start_time:.2f} seconds")
                    st.subheader("Original Transcript")
                    st.write(transcript)
                    st.markdown(f"<div style='color: white;'>Detected language: {detected_lang}</div>", unsafe_allow_html=True)
                    
                    # Translation
                    for lang in selected_languages:
                        if lang.lower() != detected_lang:
                            try:
                                translated_text = translate_text(transcript, lang)
                                if translated_text:
                                    st.subheader(f"{lang} Translation")
                                    st.write(translated_text)
                                    
                                    st.download_button(
                                        label=f"Download {lang} translation",
                                        data=translated_text,
                                        file_name=f"translation_{lang}.txt",
                                        mime="text/plain"
                                    )
                                else:
                                    st.warning(f"Translation to {lang} failed.")
                            except OpenAIError as e:
                                st.error(f"An error occurred during translation to {lang}: {str(e)}")
                        else:
                            st.markdown(f"<div style='color: white;'>Skipping translation to {lang} as it's the detected original language.</div>", unsafe_allow_html=True)
                    
                    progress_bar.progress(100)
                    status_text.text("Processing complete!")
                else:
                    st.error("Transcription failed. The audio file may be corrupted or empty.")
            except Exception as e:
                st.error(f"An error occurred during processing: {str(e)}")
        else:
            st.error("Failed to convert video to audio. The video file may be corrupted or in an unsupported format.")
        
        # Clean up temporary files
        for temp_file in [TEMP_VIDEO, TEMP_AUDIO]:
            if os.path.exists(temp_file):
                os.remove(temp_file)

# Add the application description at the bottom left
st.markdown("<div class='app-description'>This application converts video files to audio, creates transcripts, and translates to selected languages.</div>", unsafe_allow_html=True)

# FFmpeg info at the bottom right
st.markdown("<div style='position: fixed; right: 10px; bottom: 10px; font-size: 0.8em; color: rgba(255,255,255,0.5);'>FFmpeg (c) 2000-2024</div>", unsafe_allow_html=True)