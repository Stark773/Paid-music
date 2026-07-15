import os
import re
import textwrap
import numpy as np
import aiofiles
import aiohttp
from PIL import (
    Image,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageFont,
    ImageOps,
)
from py_yt import VideosSearch
from config import YOUTUBE_IMG_URL


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    ratio = min(widthRatio, heightRatio)
    newWidth = int(image.size[0] * ratio)
    newHeight = int(image.size[1] * ratio)
    try:
        resample = Image.Resampling.LANCZOS
    except AttributeError:
        resample = Image.ANTIALIAS
    return image.resize((newWidth, newHeight), resample)


def get_dominant_color(image):
    image = image.convert("RGB").resize((50, 50))
    pixels = np.array(image).reshape(-1, 3)
    avg = tuple(pixels.mean(axis=0).astype(int))
    if sum(avg) < 200:
        avg = tuple(min(255, int(c * 1.5)) for c in avg)
    return avg


def get_contrasting_color(bg):
    lum = 0.299 * bg[0] + 0.587 * bg[1] + 0.114 * bg[2]
    return (255, 255, 255) if lum < 128 else (30, 30, 30)


def safe_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def rounded_rectangle(draw, xy, radius, fill):
    x1, y1, x2, y2 = xy
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.ellipse([x1, y1, x1 + 2 * radius, y1 + 2 * radius], fill=fill)
    draw.ellipse([x2 - 2 * radius, y1, x2, y1 + 2 * radius], fill=fill)
    draw.ellipse([x1, y2 - 2 * radius, x1 + 2 * radius, y2], fill=fill)
    draw.ellipse([x2 - 2 * radius, y2 - 2 * radius, x2, y2], fill=fill)


async def get_thumb(videoid):
    final_path = f"cache/{videoid}.png"
    if os.path.isfile(final_path):
        return final_path

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        result_data = await results.next()
        if not result_data.get("result"):
            return YOUTUBE_IMG_URL

        result = result_data["result"][0]
        title = re.sub(r"\W+", " ", result.get("title", "Unknown Title")).title()
        duration = result.get("duration", "Unknown")
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        views = result.get("viewCount", {}).get("short", "Unknown")
        channel = result.get("channel", {}).get("name", "Unknown")

        os.makedirs("cache", exist_ok=True)

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                thumb_path = f"cache/thumb{videoid}.png"
                async with aiofiles.open(thumb_path, mode="wb") as f:
                    await f.write(await resp.read())

        try:
            youtube = Image.open(thumb_path).convert("RGBA")
        except Exception:
            if os.path.exists(thumb_path):
                os.remove(thumb_path)
            return YOUTUBE_IMG_URL

        # --- Canvas ---
        W, H = 1280, 720
        canvas = Image.new("RGBA", (W, H), (10, 10, 20, 255))

        # Blurred bg from thumbnail
        bg = changeImageSize(W, H, youtube.copy().convert("RGBA"))
        bg_blur = bg.filter(ImageFilter.GaussianBlur(radius=22))
        bg_dark = ImageEnhance.Brightness(bg_blur).enhance(0.35)
        # Expand to fill canvas
        bg_full = Image.new("RGBA", (W, H), (10, 10, 20, 255))
        bx = (W - bg_dark.width) // 2
        by = (H - bg_dark.height) // 2
        bg_full.paste(bg_dark, (bx, by))
        canvas.paste(bg_full, (0, 0))

        # Gradient overlay (bottom fade)
        grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        grad_draw = ImageDraw.Draw(grad)
        for i in range(H // 2, H):
            alpha = int(200 * (i - H // 2) / (H // 2))
            grad_draw.line([(0, i), (W, i)], fill=(0, 0, 0, alpha))
        canvas = Image.alpha_composite(canvas, grad)

        # Dominant color for accent
        accent = get_dominant_color(youtube.convert("RGB"))
        accent_light = tuple(min(255, int(c * 1.4)) for c in accent)

        # --- Thumbnail card (left side) ---
        CARD_W, CARD_H = 520, 380
        card_x, card_y = 60, 120

        # Glow behind card
        glow = Image.new("RGBA", (CARD_W + 40, CARD_H + 40), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.rounded_rectangle([0, 0, CARD_W + 40, CARD_H + 40], radius=30,
                              fill=(*accent, 80))
        canvas.alpha_composite(glow, (card_x - 20, card_y - 20))

        # Card background
        card_bg = Image.new("RGBA", (CARD_W, CARD_H), (20, 20, 30, 220))
        card_mask = Image.new("L", (CARD_W, CARD_H), 0)
        ImageDraw.Draw(card_mask).rounded_rectangle(
            [0, 0, CARD_W, CARD_H], radius=20, fill=255
        )
        canvas.paste(card_bg, (card_x, card_y), card_mask)

        # Thumbnail inside card
        thumb_inner = changeImageSize(CARD_W - 20, CARD_H - 20, youtube.convert("RGBA"))
        ti_mask = Image.new("L", thumb_inner.size, 0)
        ImageDraw.Draw(ti_mask).rounded_rectangle(
            [0, 0, thumb_inner.width, thumb_inner.height], radius=16, fill=255
        )
        tx = card_x + (CARD_W - thumb_inner.width) // 2
        ty = card_y + (CARD_H - thumb_inner.height) // 2
        canvas.paste(thumb_inner, (tx, ty), ti_mask)

        # Accent border on card
        border_layer = Image.new("RGBA", (CARD_W + 4, CARD_H + 4), (0, 0, 0, 0))
        ImageDraw.Draw(border_layer).rounded_rectangle(
            [0, 0, CARD_W + 3, CARD_H + 3], radius=22,
            outline=(*accent_light, 200), width=3
        )
        canvas.alpha_composite(border_layer, (card_x - 2, card_y - 2))

        # --- Right panel text ---
        draw = ImageDraw.Draw(canvas)
        rx = card_x + CARD_W + 60
        ry = card_y + 10

        # Bot watermark pill
        font_brand = safe_font("Muskan/assets/font2.ttf", 22)
        brand_text = "🎵 MUSKAN MUSIC"
        bbox = draw.textbbox((0, 0), brand_text, font=font_brand)
        bw = bbox[2] - bbox[0] + 30
        bh = bbox[3] - bbox[1] + 14
        pill_layer = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        ImageDraw.Draw(pill_layer).rounded_rectangle(
            [0, 0, bw, bh], radius=bh // 2,
            fill=(*accent, 220)
        )
        canvas.alpha_composite(pill_layer, (rx, ry))
        draw.text((rx + 15, ry + 7), brand_text, font=font_brand, fill=(255, 255, 255, 255))
        ry += bh + 22

        # Title
        font_title = safe_font("Muskan/assets/font.ttf", 38)
        short_title = textwrap.shorten(title, width=28, placeholder="…")
        draw.text((rx, ry), short_title, font=font_title, fill=(255, 255, 255, 255))
        ry += 52

        # Channel
        font_meta = safe_font("Muskan/assets/font2.ttf", 26)
        draw.text((rx, ry), f"📺  {channel[:28]}", font=font_meta, fill=(*accent_light, 230))
        ry += 40

        # Views
        draw.text((rx, ry), f"👁  {views[:20]}", font=font_meta, fill=(200, 200, 200, 200))
        ry += 40

        # Duration
        draw.text((rx, ry), f"⏱  {duration}", font=font_meta, fill=(200, 200, 200, 200))
        ry += 55

        # Divider
        draw.line([(rx, ry), (W - 60, ry)], fill=(*accent, 160), width=2)
        ry += 18

        # Progress bar area
        bar_x1 = rx
        bar_x2 = W - 60
        bar_y = ry + 10
        bar_h = 8
        bar_w = bar_x2 - bar_x1
        # Track background
        draw.rounded_rectangle([bar_x1, bar_y, bar_x2, bar_y + bar_h],
                                radius=4, fill=(60, 60, 80, 200))
        # Filled portion (~15%)
        fill_end = bar_x1 + int(bar_w * 0.15)
        draw.rounded_rectangle([bar_x1, bar_y, fill_end, bar_y + bar_h],
                                radius=4, fill=(*accent_light, 255))
        # Dot
        draw.ellipse([fill_end - 7, bar_y - 4, fill_end + 7, bar_y + bar_h + 4],
                     fill=(255, 255, 255, 255))
        # Time labels
        font_time = safe_font("Muskan/assets/font2.ttf", 22)
        draw.text((bar_x1, bar_y + bar_h + 8), "00:00", font=font_time, fill=(180, 180, 180, 200))
        draw.text((bar_x2 - 60, bar_y + bar_h + 8), duration[:8], font=font_time, fill=(180, 180, 180, 200))

        # --- Bottom strip ---
        strip_y = H - 48
        strip = Image.new("RGBA", (W, 48), (0, 0, 0, 0))
        ImageDraw.Draw(strip).rectangle([0, 0, W, 48], fill=(*accent, 50))
        canvas.alpha_composite(strip, (0, strip_y))
        font_strip = safe_font("Muskan/assets/font2.ttf", 20)
        draw.text(
            (40, strip_y + 14),
            "🎵  Muskan Music  •  Your Perfect Music Companion",
            font=font_strip,
            fill=(230, 230, 230, 200),
        )

        try:
            os.remove(thumb_path)
        except Exception:
            pass

        out = canvas.convert("RGB")
        out.save(final_path, format="PNG")
        return final_path

    except Exception:
        return YOUTUBE_IMG_URL
