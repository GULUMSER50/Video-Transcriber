import subprocess
import os
from config import TEMP_AUDIO

def convert_video_to_audio(video_file):
    try:
        command = f"ffmpeg -i {video_file} -acodec pcm_s16le -ac 1 -ar 16000 {TEMP_AUDIO}"
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"FFmpeg stdout: {result.stdout}")
        print(f"FFmpeg stderr: {result.stderr}")
        return TEMP_AUDIO if os.path.exists(TEMP_AUDIO) else None
    except subprocess.CalledProcessError as e:
        print(f"Error during video to audio conversion: {e}")
        print(f"FFmpeg stdout: {e.stdout}")
        print(f"FFmpeg stderr: {e.stderr}")
        return None