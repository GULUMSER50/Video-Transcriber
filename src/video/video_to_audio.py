import os
from moviepy.editor import VideoFileClip
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def extract_audio(video_path, output_path):
    try:
        video_path = Path(video_path)
        output_path = Path(output_path)
        
        # Ensure the output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Expand the list of supported video formats
        supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
        
        # Check if any supported format is in the filename
        if not any(fmt in video_path.name.lower() for fmt in supported_formats):
            raise ValueError(f"Unsupported video format. Please use one of these formats: {', '.join(supported_formats)}")
        
        logger.info(f"Attempting to extract audio from: {video_path}")
        video = VideoFileClip(str(video_path))
        
        if video.audio is None:
            raise ValueError("The video file does not contain an audio track.")
        
        audio = video.audio
        audio.write_audiofile(str(output_path))
        video.close()
        
        logger.info(f"Audio extracted and saved to {output_path}")
        return str(output_path)
    except Exception as e:
        logger.error(f"Error extracting audio: {str(e)}")
        return None