import subprocess
import tempfile
import os
import logging

logger = logging.getLogger(__name__)

def convert_audio(audio_data: bytes, from_format: str, to_format: str) -> bytes:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{from_format}") as temp_in:
            temp_in.write(audio_data)
            temp_in_path = temp_in.name
            
        temp_out_path = temp_in_path.rsplit(".", 1)[0] + f".{to_format}"
        
        command = [
            "ffmpeg", "-y", "-i", temp_in_path, "-f", to_format, temp_out_path
        ]
        
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        with open(temp_out_path, "rb") as f:
            converted_data = f.read()
            
        return converted_data
    except Exception as e:
        logger.error(f"Audio conversion error (ffmpeg might not be installed): {e}")
        return audio_data  # Fallback to original
    finally:
        if 'temp_in_path' in locals() and os.path.exists(temp_in_path):
            os.remove(temp_in_path)
        if 'temp_out_path' in locals() and os.path.exists(temp_out_path):
            os.remove(temp_out_path)

def get_audio_duration(audio_data: bytes) -> float:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as temp_in:
            temp_in.write(audio_data)
            temp_in_path = temp_in.name
            
        command = [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration", "-of",
            "default=noprint_wrappers=1:nokey=1", temp_in_path
        ]
        
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        duration = float(result.stdout.decode().strip())
        return duration
    except Exception as e:
        logger.error(f"Error getting audio duration: {e}")
        return 0.0
    finally:
        if 'temp_in_path' in locals() and os.path.exists(temp_in_path):
            os.remove(temp_in_path)

def compress_audio(audio_data: bytes, target_bitrate: str = "16k") -> bytes:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as temp_in:
            temp_in.write(audio_data)
            temp_in_path = temp_in.name
            
        temp_out_path = temp_in_path + "_compressed.mp3"
        
        command = [
            "ffmpeg", "-y", "-i", temp_in_path, "-b:a", target_bitrate, "-f", "mp3", temp_out_path
        ]
        
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        with open(temp_out_path, "rb") as f:
            compressed_data = f.read()
            
        return compressed_data
    except Exception as e:
        logger.error(f"Audio compression error: {e}")
        return audio_data  # Fallback to original
    finally:
        if 'temp_in_path' in locals() and os.path.exists(temp_in_path):
            os.remove(temp_in_path)
        if 'temp_out_path' in locals() and os.path.exists(temp_out_path):
            os.remove(temp_out_path)
