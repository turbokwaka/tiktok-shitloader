# main.py

import random
import urllib
import warnings

from voice_overlay import generate_tts, merge
from subtitles_overlay import transcribe_and_subtitle_video

import uuid
import os
import logging

logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%H:%M:%S", level=logging.INFO
)
warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BIN_DIR = os.path.join(BASE_DIR, "bin")
TEMP_PATH = os.path.join(BASE_DIR, "temp")
INPUT_PATH = os.path.join(BASE_DIR, "input")
BG_VIDEOS_PATH = os.path.join(INPUT_PATH, "bg_videos")
INPUT_TEXT_PATH = os.path.join(INPUT_PATH, "input.txt")
OUTPUT_VIDEO_PATH = os.path.join(BASE_DIR, "output")

FILES_TO_DOWNLOAD = {
    "voices-v1.0.bin": "https://github.com/nazdridoy/kokoro-tts/releases/download/v1.0.0/voices-v1.0.bin",
    "kokoro-v1.0.onnx": "https://github.com/nazdridoy/kokoro-tts/releases/download/v1.0.0/kokoro-v1.0.onnx",
}


def ensure_voice_models():
    os.makedirs(BIN_DIR, exist_ok=True)
    for filename, url in FILES_TO_DOWNLOAD.items():
        path = os.path.join(BIN_DIR, filename)
        if not os.path.exists(path):
            logging.info(f"Завантажую {filename} ...")
            urllib.request.urlretrieve(url, path)
            logging.info(f"Завантажено {filename}")


def main(
    input_text_path: str = INPUT_TEXT_PATH,
    bg_videos_path: str = BG_VIDEOS_PATH,
    output_video_path: str = OUTPUT_VIDEO_PATH,
):
    logging.info("Погналі!")

    if not os.path.exists(output_video_path):
        os.makedirs(output_video_path)
        logging.info(f"Створено тимчасову папку: {output_video_path}")

    if not os.path.exists(output_video_path):
        os.makedirs(output_video_path)
        logging.info(f"Створено вихідну папку: {output_video_path}")

    ensure_voice_models()

    output_audio_path = os.path.join(TEMP_PATH, f"{uuid.uuid4()}.wav")
    no_subtitles_video_path = os.path.join(TEMP_PATH, f"{uuid.uuid4()}.mp4")
    output_subtitled_video_path = os.path.join(output_video_path, f"{uuid.uuid4()}.mp4")

    logging.info("Створюємо аудіо з тексту...")
    generate_tts(input_text_path, output_audio_path)

    no_subtitles_video_path = os.path.join(TEMP_PATH, f"{str(uuid.uuid4())}.mp4")

    files = [f for f in os.listdir(bg_videos_path) if f.endswith(".mp4")]
    if not files:
        raise FileNotFoundError(f"Не знайдено жодного .mp4 у {bg_videos_path}")
    bg_video_path = os.path.join(bg_videos_path, random.choice(files))
    logging.info("Накладаємо аудіо на відео...")
    merge(bg_video_path, output_audio_path, no_subtitles_video_path)
    os.remove(output_audio_path)

    logging.info("Створюємо субтитри...")
    transcribe_and_subtitle_video(
        no_subtitles_video_path,
        output_subtitled_video_path,
        font_size=96,
        lang="en",
        model_name="tiny",
    )
    os.remove(no_subtitles_video_path)

    logging.info(
        f"Готово! Відео з субтитрами збережено у: {output_subtitled_video_path}"
    )


if __name__ == "__main__":
    main()
