import subprocess
import os


class AudioExtractor:
    def __init__(self, video_path, audio_output_path):
        self.video_path = video_path
        self.audio_output_path = audio_output_path

    def extract_audio(self):
        try:
            # Verify input file exists
            if not os.path.exists(self.video_path):
                print(f"Error: Video file {self.video_path} does not exist")
                return None

            command = [
                "ffmpeg", "-y", "-i", self.video_path,
                "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
                self.audio_output_path
            ]
            result = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                print(f"🎵 Extracted audio to {self.audio_output_path}")
                return self.audio_output_path
            else:
                print(f"Error extracting audio: {result.stderr}")
                return None
        except Exception as e:
            print(f"Error during audio extraction: {e}")
            return None