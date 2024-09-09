import os
from moviepy.editor import VideoFileClip
from ..utils.helpers import ensure_dir, get_file_extension

def extract_audio(video_path, output_path):
    try:
        ensure_dir(os.path.dirname(output_path))
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        video = VideoFileClip(video_path)
        audio = video.audio
        
        if get_file_extension(output_path).lower() != '.wav':
            output_path = output_path.rsplit('.', 1)[0] + '.wav'
        
        audio.write_audiofile(output_path)
        video.close()
        audio.close()
        
        print(f"Audio extracted and saved to {output_path}")
        return output_path
    except Exception as e:
        print(f"Error extracting audio: {str(e)}")
        return None