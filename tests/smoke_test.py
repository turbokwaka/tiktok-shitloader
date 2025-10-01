# smoke_test.py

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
import warnings
from pathlib import Path

import pytest
from main import main, OUTPUT_VIDEO_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_VIDEO_DIR = os.path.join(BASE_DIR, "input", "bg_videos")
INPUT_TEXT_PATH = os.path.join(BASE_DIR, "input", "input.txt")


logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%H:%M:%S", level=logging.INFO
)
warnings.filterwarnings("ignore")


def test_pipeline_smoke():
    output_dir = Path(OUTPUT_VIDEO_PATH)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        main(input_text_path=INPUT_TEXT_PATH, bg_videos_path=INPUT_VIDEO_DIR)
    except Exception as e:
        pytest.fail(f"Пайплайн впав з помилкою: {e}")

    mp4_files = list(output_dir.glob("*.mp4"))
    assert mp4_files, f"Фінальний відеофайл не створився у {output_dir.resolve()}"
