# subtitles_overlay.py

import numpy as np
import whisper_timestamped as whisper
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy import ImageClip
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_DIRECTORY = os.path.join(BASE_DIR, "output")
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")


def make_caption_image(
    text,
    font_path=os.path.join(FONTS_DIR, "Montserrat-Bold.ttf"),
    font_size=72,
    text_color=(255, 214, 10),
    glow_color=(255, 90, 0),
    padding_x=50,
    padding_y=30,
):
    font = ImageFont.truetype(font_path, font_size)

    dummy_img = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    img_w, img_h = text_w + 2 * padding_x, text_h + 2 * padding_y
    img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))

    text_x = (img_w - text_w) // 2
    text_y = (img_h - text_h) - 100 // 2
    text_pos = (text_x, text_y)

    glow = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.text(text_pos, text, font=font, fill=glow_color + (255,))
    glow1 = glow.filter(ImageFilter.GaussianBlur(radius=3))
    glow2 = glow.filter(ImageFilter.GaussianBlur(radius=10))
    img = Image.alpha_composite(glow1, img)
    img = Image.alpha_composite(glow2, img)

    draw = ImageDraw.Draw(img)
    draw.text(text_pos, text, font=font, fill=text_color + (255,))

    return img


def split_segments_to_short_phrases(result, words_per_chunk=3):
    short_subs = []

    for seg in result["segments"]:
        words = seg.get("words", [])
        if not words:
            continue

        for i in range(0, len(words), words_per_chunk):
            chunk = words[i : i + words_per_chunk]
            start_time = float(chunk[0]["start"])
            end_time = float(chunk[-1]["end"])
            text = " ".join([w["text"].strip() for w in chunk])
            short_subs.append(((start_time, end_time), text))

    return short_subs


def transcribe_and_subtitle_video(
    video_path,
    output_path,
    font_path=os.path.join(FONTS_DIR, "Montserrat-Bold.ttf"),
    font_size=32,
    words_per_chunk=2,
    lang="en",
    model_name="tiny",
):
    if not os.path.exists(video_path):
        print(f"Помилка: Відео файл не знайдено за шляхом '{video_path}'")
        return

    model = whisper.load_model(model_name, device="cpu")
    result = whisper.transcribe(model, video_path, language=lang, verbose=False)
    subtitles = split_segments_to_short_phrases(result, words_per_chunk)

    clip = VideoFileClip(f"{video_path}").subclipped(0, None).with_volume_scaled(0.8)

    subtitle_clips = []
    for (start, end), text in subtitles:
        img = make_caption_image(text, font_path, font_size)
        img_array = np.array(img)
        txt = (
            ImageClip(img_array, transparent=True)
            .with_start(float(start))
            .with_duration(float(end - start))
            .with_position(
                lambda t: ("center", clip.h / 2 + 100 + 50 * (1 - min(1, t / 0.1)))
            )
            .resized(lambda t: 0.7 + 0.3 * min(1, t / 0.05))
        )
        subtitle_clips.append(txt)

    final_video = CompositeVideoClip([clip] + subtitle_clips)
    final_video.write_videofile(f"{output_path}", logger=None)
