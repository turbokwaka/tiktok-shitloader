# voice_overlay.py
import logging
import os
import subprocess
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_TEXT_PATH = os.path.join(BASE_DIR, "input", "input.txt")
INPUT_VIDEO_PATH = os.path.join(BASE_DIR, "input", "bg_videos", "1.mp4")
TEMP_PATH = os.path.join(BASE_DIR, "temp")


def generate_tts(input_txt, output_wav):
    cmd = [
        "kokoro-tts",
        input_txt,
        output_wav,
        "--model",
        os.path.join(BASE_DIR, "bin", "kokoro-v1.0.onnx"),
        "--voices",
        os.path.join(BASE_DIR, "bin", "voices-v1.0.bin"),
        "--voice",
        "af_heart",
    ]
    try:
        subprocess.run(
            cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError as e:
        logging.error(e.output)


def merge(video_path, audio_path, output_path):
    videoclip = VideoFileClip(video_path)
    audioclip = AudioFileClip(audio_path)
    audioclip_duration = audioclip.duration
    videoclip = videoclip.subclipped(0, audioclip_duration)
    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    videoclip.write_videofile(output_path, logger=None)
