# voice_overlay.py

import subprocess
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip

INPUT_TEXT_PATH = "input/input.txt"
INPUT_VIDEO_PATH = "bg_videos/1.mp4"

def generate_tts(input_txt, output_wav):
    cmd = [
        "kokoro-tts",
        input_txt,
        output_wav,
        "--model", "bin/kokoro-v1.0.onnx",
        "--voices", "bin/voices-v1.0.bin",
        "--voice", "af_heart"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def merge(video_path, audio_path, output_path):
    videoclip = VideoFileClip(video_path)
    audioclip = AudioFileClip(audio_path)
    audioclip_duration = audioclip.duration
    videoclip = videoclip.subclipped(0, audioclip_duration)
    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    videoclip.write_videofile(output_path, logger=None)