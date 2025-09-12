from PIL import Image, ImageDraw, ImageFont, ImageFilter

def make_caption_image(text, font_path="fonts/Montserrat-Bold.ttf", font_size=72,
                       text_color=(255, 214, 10), glow_color=(255, 90, 0),
                       padding_x=50, padding_y=30):
    # шрифт
    font = ImageFont.truetype(font_path, font_size)

    # bounding box тексту
    dummy_img = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # розмір картинки з урахуванням padding
    img_w, img_h = text_w + 2 * padding_x, text_h + 2 * padding_y
    img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))

    # центруємо текст по картинці
    text_x = (img_w - text_w) // 2
    text_y = (img_h - text_h) - 100 // 2
    text_pos = (text_x, text_y)

    # --- glow ---
    glow = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.text(text_pos, text, font=font, fill=glow_color + (255,))
    glow1 = glow.filter(ImageFilter.GaussianBlur(radius=3))
    glow2 = glow.filter(ImageFilter.GaussianBlur(radius=10))
    img = Image.alpha_composite(glow1, img)
    img = Image.alpha_composite(glow2, img)

    # --- основний текст ---
    draw = ImageDraw.Draw(img)
    draw.text(text_pos, text, font=font, fill=text_color + (255,))

    return img

result=make_caption_image(text="Hello World", font_path="fonts/Chewy-Regular.ttf")

# Відкрити для перегляду у вікні (не в браузері)
result.show()  # відкриє стандартний переглядач зображень