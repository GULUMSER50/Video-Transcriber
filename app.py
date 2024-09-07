import streamlit as st
import os
import subprocess
import time
from openai import RateLimitError
from config import LANGUAGES, TEMP_VIDEO, TEMP_AUDIO
from video_to_audio import convert_video_to_audio
from audio_to_text import transcribe_audio
from text_translation import translate_text

st.title("Video Transcriber and Translator")

# Add this block to display FFmpeg version information
ffmpeg_version = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout
st.sidebar.text("FFmpeg Version Info:")
st.sidebar.text(ffmpeg_version.split("\n")[0])  # Display only the first line of FFmpeg version info

selected_languages = st.multiselect("Select languages for translation:", LANGUAGES)

uploaded_file = st.file_uploader("Upload video file", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    with st.spinner("Processing video..."):
        with open(TEMP_VIDEO, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.text("Converting video to audio...")
        audio_file = convert_video_to_audio(TEMP_VIDEO)
        
        if audio_file:
            try:
                with st.spinner("Transcribing audio..."):
                    start_time = time.time()
                    transcript, detected_lang = transcribe_audio(audio_file)
                    end_time = time.time()
                
                st.success(f"Transcription completed in {end_time - start_time:.2f} seconds")
                
                if transcript:
                    st.subheader("Original Transcript:")
                    st.write(transcript)
                    st.write(f"Detected language: {detected_lang}")
                    
                    for lang in selected_languages:
                        if lang.lower() != detected_lang:
                            try:
                                with st.spinner(f"Translating to {lang}..."):
                                    translated_text = translate_text(transcript, lang)
                                st.subheader(f"{lang} Translation:")
                                st.write(translated_text)
                                
                                st.download_button(
                                    label=f"Download {lang} translation",
                                    data=translated_text,
                                    file_name=f"translation_{lang}.txt",
                                    mime="text/plain"
                                )
                            except RateLimitError:
                                st.warning(f"Translation to {lang} skipped due to API rate limit. Please check your OpenAI API quota.")
                            except Exception as e:
                                st.error(f"An error occurred during translation to {lang}: {str(e)}")
                        else:
                            st.info(f"Skipping translation to {lang} as it's the detected original language.")
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

st.info("This application converts video files to audio, creates transcripts, and translates to selected languages.")