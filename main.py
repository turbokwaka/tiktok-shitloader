import random
import warnings

from voice_overlay import generate_tts, merge, INPUT_VIDEO_PATH
from subtitles_overlay import transcribe_and_subtitle_video, OUTPUT_DIRECTORY

import uuid
import os
import logging

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)
warnings.filterwarnings("ignore")

TEMP_PATH = "temp"
BG_VIDEOS_PATH = "bg_videos"
INPUT_TEXT_PATH = "input/input.txt"
OUTPUT_VIDEO_PATH = "output"

def main():
    logging.info("Погналі!")

    output_audio_path = os.path.join(TEMP_PATH, f"{str(uuid.uuid4())}.wav")
    logging.info("Створюємо аудіо з тексту...")
    generate_tts(INPUT_TEXT_PATH, output_audio_path)

    no_subtitles_video_path = os.path.join(TEMP_PATH, f"{str(uuid.uuid4())}.mp4")

    files = [f for f in os.listdir(BG_VIDEOS_PATH) if f.endswith(".mp4")]
    bg_video_path = os.path.join(BG_VIDEOS_PATH, random.choice(files))
    logging.info("Накладаємо аудіо на відео...")
    merge(bg_video_path, output_audio_path, no_subtitles_video_path)
    os.remove(output_audio_path)

    output_subtitled_video_path = os.path.join(OUTPUT_DIRECTORY, f"{str(uuid.uuid4())}.mp4")
    logging.info("Створюємо субтитри...")
    transcribe_and_subtitle_video(no_subtitles_video_path, output_subtitled_video_path, font_size=96, lang="en", model_name="tiny")

    logging.info(f"Готово! Відео з субтитрами збережено у {output_subtitled_video_path}")

if __name__ == "__main__":
    main()
