from io import BytesIO
import os
import re
import random
import aiofiles
import aiohttp
from PIL import (
    Image,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageFont,
    ImageOps,
    ImageChops,
)
from py_yt import VideosSearch
from config import YOUTUBE_IMG_URL as FAILED
from BABYMUSIC import app, userbot
from BABYMUSIC.misc import db
import numpy as np

# ✅ Get the absolute path to the assets directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "..", "assets")

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# ------------------- UI CONFIG -------------------
CANVAS_W, CANVAS_H = 1280, 720
NOISE_IMG = 25
PANEL_W, PANEL_H = 820, 360          # card size
MARGIN_X, MARGIN_Y = 40, 80          # safe margin for random placement

THUMB_W, THUMB_H = 260, 260
BAR_W, BAR_H = 430, 6

USER_DP_SIZE = 80
MAX_TITLE_WIDTH = 430
TRANSPARENCY = 180
# -------------------------------------------------

GRADIENT_SETS = [
    [(255, 255, 224), (255, 239, 213), (255, 218, 185),
     (255, 182, 193), (255, 160, 122), (255, 140, 0),
     (255, 99, 71), (255, 69, 0), (178, 34, 34), (139, 0, 0)],
    [(0, 105, 148), (0, 191, 255), (70, 130, 180),
     (100, 149, 237), (65, 105, 225), (123, 104, 238),
     (138, 43, 226), (106, 90, 205), (72, 61, 139)],
    [(0, 100, 0), (34, 139, 34), (46, 139, 87),
     (60, 179, 113), (107, 142, 35), (124, 252, 0),
     (127, 255, 0), (173, 255, 47), (144, 238, 144), (152, 251, 152)],
    [(255, 192, 203), (255, 182, 193), (255, 160, 122),
     (221, 160, 221), (218, 112, 214), (238, 130, 238),
     (216, 191, 216), (186, 85, 211), (147, 112, 219)],
    [(57, 255, 20), (0, 255, 127), (0, 255, 255),
     (0, 191, 255), (30, 144, 255), (138, 43, 226),
     (255, 20, 147), (255, 0, 255), (255, 105, 180), (255, 255, 0)],
    [(224, 255, 255), (175, 238, 238), (173, 216, 230),
     (135, 206, 250), (135, 206, 235), (176, 224, 230)],
    [(111, 78, 55), (139, 69, 19), (160, 82, 45),
     (205, 133, 63), (222, 184, 135), (245, 222, 179)],
    [(26, 35, 126), (57, 73, 171), (92, 107, 192),
     (121, 134, 203), (159, 168, 218)],
    [(255, 228, 181), (255, 218, 185), (255, 160, 122),
     (244, 164, 96), (210, 105, 30), (139, 69, 19)],
    [(48, 25, 52), (75, 0, 130), (106, 90, 205),
     (123, 104, 238), (147, 112, 219)],
    [(152, 251, 152), (144, 238, 144), (102, 205, 170),
     (127, 255, 212), (175, 238, 238)],
    [(33, 33, 33), (55, 55, 55), (77, 77, 77),
     (99, 99, 99), (120, 120, 120)],
    [(0, 51, 102), (0, 76, 153), (0, 102, 204),
     (0, 128, 255), (51, 153, 255)],
    [(255, 218, 185), (255, 182, 193), (255, 160, 122),
     (250, 128, 114), (233, 150, 122)],
    [(107, 142, 35), (85, 107, 47), (143, 188, 143),
     (189, 183, 107), (240, 230, 140)],
    [(230, 230, 250), (216, 191, 216), (221, 160, 221),
     (238, 130, 238), (218, 112, 214)],
    [(0, 0, 0), (25, 25, 25), (50, 50, 50),
     (75, 75, 75), (100, 100, 100)],
    [(255, 250, 205), (255, 255, 153), (255, 255, 102),
     (255, 255, 0), (204, 204, 0)],
    [(75, 0, 130), (138, 43, 226), (148, 0, 211),
     (186, 85, 211), (218, 112, 214)],
    [(255, 127, 80), (240, 128, 128), (233, 150, 122),
     (205, 92, 92), (178, 34, 34)],
    [(245, 245, 245), (220, 220, 220), (211, 211, 211),
     (192, 192, 192), (169, 169, 169)],
]


def trim_to_width(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> str:
    ellipsis = "…"
    if font.getlength(text) <= max_w:
        return text
    for i in range(len(text) - 1, 0, -1):
        if font.getlength(text[:i] + ellipsis) <= max_w:
            return text[:i] + ellipsis
    return ellipsis

def draw_smooth_bold_text(draw, pos, text, font):
    x, y = pos

    # soft black shadow (multi-layer for smoothness)
    shadow_offsets = [
        (1, 1), (2, 2),
        (2, 1), (1, 2)
    ]
    for dx, dy in shadow_offsets:
        draw.text(
            (x + dx, y + dy),
            text,
            font=font,
            fill=(0, 0, 0, 160),
        )

    # main white text (draw twice = bold feel)
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    draw.text((x + 0.5, y), text, font=font, fill=(255, 255, 255, 255))



def make_7_color_border(size, thickness=8):
    """Random multi‑color outer border; 7 colors tak repeat karke."""
    w, h = size
    base_colors = random.choice(GRADIENT_SETS)
    n = len(base_colors)

    if n >= 7:
        colors = random.sample(base_colors, 7)
    else:
        colors = (base_colors * (7 // n + 1))[:7]

    def lerp(c1, c2, t):
        return (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t),
            255,
        )

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    perim = 2 * (w + h - 2)

    for i in range(perim):
        seg = (i * 6) // perim
        t = (i * 6) / perim - seg
        c = lerp(colors[seg], colors[min(seg + 1, 6)], t)

        if i < w:
            x, y = i, 0
        elif i < w + h - 1:
            x, y = w - 1, i - w + 1
        elif i < 2 * w + h - 2:
            x, y = w - 1 - (i - (w + h - 1)), h - 1
        else:
            x, y = 0, h - 1 - (i - (2 * w + h - 2))

        draw.rectangle((x, y, x + thickness - 1, y + thickness - 1), fill=c)
    return img

def add_3d_dp_ring(dp: Image.Image, size: int):
    """
    Add 3D ring effect:
    - inner soft black shadow
    - outer thin white stroke
    """
    canvas = Image.new("RGBA", (size + 8, size + 8), (0, 0, 0, 0))
    cx = cy = 4

    # ---------- OUTER WHITE RING ----------
    outer = Image.new("RGBA", (size + 8, size + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(outer)
    d.ellipse(
        (0, 0, size + 7, size + 7),
        outline=(255, 255, 255, 200),
        width=2,  # ultra thin
    )

    # ---------- INNER BLACK SHADOW ----------
    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse(
        (2, 2, size - 2, size - 2),
        outline=(0, 0, 0, 140),
        width=3,
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(1.2))

    # ---------- COMPOSE ----------
    canvas.alpha_composite(shadow, (cx, cy))
    canvas.alpha_composite(dp, (cx, cy))
    canvas.alpha_composite(outer, (0, 0))

    return canvas


def add_bg_bubbles(bg, count=8):
    """
    Background-only glass bubbles (draw BEFORE panel)
    """
    w, h = bg.size

    for _ in range(count):
        r = random.randint(70, 180)
        x = random.randint(0, w - r * 2)
        y = random.randint(0, h - r * 2)

        # crop background area
        patch = bg.crop((x, y, x + r * 2, y + r * 2))
        patch = patch.filter(ImageFilter.GaussianBlur(20))

        # circular mask
        mask = Image.new("L", (r * 2, r * 2), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, r * 2, r * 2), fill=160)

        bubble = Image.new("RGBA", (r * 2, r * 2), (255, 255, 255, 0))
        bubble.paste(patch, (0, 0), mask)

        # light glass shine
        shine = Image.new("RGBA", (r * 2, r * 2), (255, 255, 255, 0))
        d = ImageDraw.Draw(shine)
        d.ellipse(
            (r * 0.25, r * 0.25, r * 1.1, r * 1.1),
            fill=(255, 255, 255, 50),
        )
        shine = shine.filter(ImageFilter.GaussianBlur(10))

        bubble = Image.alpha_composite(bubble, shine)

        bg.alpha_composite(bubble, (x, y))

def draw_now_playing_tag(bg, draw, tag_x, tag_y, font):
    tag_w, tag_h = 170, 40
    radius = 18

    # base plate (for mask)
    tag_mask = Image.new("L", (tag_w, tag_h), 0)
    mdraw = ImageDraw.Draw(tag_mask)
    mdraw.rounded_rectangle((0, 0, tag_w, tag_h), radius, fill=255)

    # gradient plate (top light, bottom dark)
    plate = Image.new("RGBA", (tag_w, tag_h), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(plate)
    top_col = (255, 190, 230, 255)   # light pink
    mid_col = (255, 153, 204, 255)   # main
    bot_col = (220, 80, 160, 255)    # darker

    for y in range(tag_h):
        t = y / max(tag_h - 1, 1)
        if t < 0.5:
            # top -> mid
            tt = t / 0.5
            r = int(top_col[0] + (mid_col[0] - top_col[0]) * tt)
            g = int(top_col[1] + (mid_col[1] - top_col[1]) * tt)
            b = int(top_col[2] + (mid_col[2] - top_col[2]) * tt)
        else:
            # mid -> bottom
            tt = (t - 0.5) / 0.5
            r = int(mid_col[0] + (bot_col[0] - mid_col[0]) * tt)
            g = int(mid_col[1] + (bot_col[1] - mid_col[1]) * tt)
            b = int(mid_col[2] + (bot_col[2] - mid_col[2]) * tt)
        pdraw.line([(0, y), (tag_w, y)], fill=(r, g, b, 255))

    # inner highlight (pressed / glassy feel)
    highlight = Image.new("L", (tag_w, tag_h), 0)
    hdraw = ImageDraw.Draw(highlight)
    hdraw.rounded_rectangle(
        (4, 3, tag_w - 4, tag_h // 2),
        radius - 6,
        fill=80,
    )
    plate.putalpha(tag_mask)
    plate = plate.filter(ImageFilter.GaussianBlur(0.5))
    # apply highlight as extra alpha brightness on top half
    alpha = plate.split()[-1]
    alpha = ImageChops.lighter(alpha, highlight)
    plate.putalpha(alpha)

    # outer glow behind plate
    glow = Image.new("RGBA", (tag_w + 16, tag_h + 16), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.rounded_rectangle(
        (8, 8, tag_w + 8, tag_h + 8),
        radius + 8,
        fill=(255, 120, 200, 120),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(8))

    # soft shadow (pressed feel – slightly bottom)
    shadow = Image.new("RGBA", (tag_w + 8, tag_h + 8), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle(
        (4, 6, tag_w + 4, tag_h + 6),
        radius + 4,
        fill=(0, 0, 0, 140),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))

    # paste glow + shadow + plate
    bg.alpha_composite(glow, (tag_x - 8, tag_y - 8))
    bg.alpha_composite(shadow, (tag_x - 4, tag_y - 2))
    bg.alpha_composite(plate, (tag_x, tag_y))

    # text glow (inner)
    text = "NOW PLAYING"
    tx = tag_x + (tag_w - font.getlength(text)) // 2
    ty = tag_y + (tag_h - font.size) // 2 - 1

    # blurred bright text as glow
    glow_layer = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    gldraw = ImageDraw.Draw(glow_layer)
    gldraw.text((tx, ty), text, font=font, fill=(255, 255, 255, 220))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(3))
    bg.alpha_composite(glow_layer)

    # sharp main text (slight top highlight, bottom shadow feel)
    draw.text(
        (tx, ty + 1),
        text,
        font=font,
        fill=(255, 240, 255, 255),
        stroke_width=2,
        stroke_fill=(180, 40, 120, 200),
    )

def pick_random_panel_pos():
    """Har thumbnail ke liye panel ko random jagah par shift karo."""
    max_x = CANVAS_W - PANEL_W - MARGIN_X
    max_y = CANVAS_H - PANEL_H - MARGIN_Y
    x = random.randint(MARGIN_X, max_x)
    y = random.randint(MARGIN_Y, max_y)
    return x, y


async def download_and_process_profile_pic(user_id: int, size=96):
    try:
        chat = await app.get_chat(user_id)
        if not chat.photo:
            return None

        path = await app.download_media(
            chat.photo.big_file_id,
            file_name=f"cache/{user_id}.jpg"
        )

        with Image.open(path).convert("RGBA") as im:
            im = ImageOps.fit(im, (size, size))
            mask = Image.new("L", (size, size), 0)
            ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
            im.putalpha(mask)
            return im

    except Exception:
        return None



def get_user_id_from_chat(chat_id: int):
    try:
        if chat_id in db and db[chat_id]:
            return db[chat_id][0].get("user_id")
    except Exception:
        pass
    return None


async def get_thumb(videoid: str, user_id: int = None) -> str:
    """Reference design style thumbnail, panel + dots random position."""
    cache_path = os.path.join(CACHE_DIR, f"{videoid}_ref_random_v1.jpg")
    if os.path.exists(cache_path):
        try:
            os.remove(cache_path)
        except:
            pass

    results = VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1)
    try:
        data = (await results.next()).get("result", [])[0]
        raw_title = data.get("title", "Unsupported Title")
        title = re.sub(r"\s+", " ", raw_title)
        thumb_url = data.get("thumbnails", [{}])[0].get("url", FAILED)
        duration = data.get("duration") or "Live"
        views = data.get("viewCount", {}).get("short", "Unknown views")
        channel = data.get("channel", {}).get("name", "YouTube")
    except Exception:
        title, thumb_url = "Unsupported Title", FAILED
        duration, views, channel = "Live", "Unknown views", "YouTube"

    thumb_dl = os.path.join(CACHE_DIR, f"thumb{videoid}.jpg")
    async with aiohttp.ClientSession() as session:
        async with session.get(thumb_url) as resp:
            if resp.status == 200:
                async with aiofiles.open(thumb_dl, "wb") as f:
                    await f.write(await resp.read())

    base = Image.open(thumb_dl).resize((CANVAS_W, CANVAS_H)).convert("RGBA")

    # blurred background
    bg = ImageEnhance.Brightness(
        base.filter(ImageFilter.GaussianBlur(18))
    ).enhance(0.55)

    # 🔮 BACKGROUND bubbles (panel se pehle)
    add_bg_bubbles(bg, count=random.randint(6, 10))
    # panel position har baar random
    panel_x, panel_y = pick_random_panel_pos()
    panel_box = (panel_x, panel_y, panel_x + PANEL_W, panel_y + PANEL_H)

    # derived coordinates
    thumb_x, thumb_y = panel_x + 40, panel_y + 40
    right_x = thumb_x + THUMB_W + 50
    title_y = thumb_y
    meta_y = title_y + 60
    bar_y = meta_y + 70
    user_dp_x = panel_x + PANEL_W - USER_DP_SIZE - 35
    user_dp_y = panel_y + PANEL_H - USER_DP_SIZE - 35

    # dark inner panel
    panel = Image.new("RGBA", (PANEL_W, PANEL_H), (0, 0, 0, TRANSPARENCY))
    mask = Image.new("L", (PANEL_W, PANEL_H), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, PANEL_W, PANEL_H), 30, fill=255
    )
    bg.paste(panel, (panel_x, panel_y), mask)

    

    # 7‑color outer border
    border_img = make_7_color_border(
        (PANEL_W + 16, PANEL_H + 16), thickness=6
    )
    bg.alpha_composite(border_img, (panel_x - 8, panel_y - 8))

    # left rounded thumbnail
    cover = base.resize((THUMB_W, THUMB_H))
    cov_mask = Image.new("L", (THUMB_W, THUMB_H), 0)
    ImageDraw.Draw(cov_mask).rounded_rectangle(
        (0, 0, THUMB_W, THUMB_H), 20, fill=255
    )
    bg.paste(cover, (thumb_x, thumb_y), cov_mask)

    draw = ImageDraw.Draw(bg)
    try:
        # ✅ Updated font paths using ASSETS_DIR
        title_font = ImageFont.truetype(os.path.join(ASSETS_DIR, "airstrikeplat.ttf"), 34)
        meta_font = ImageFont.truetype(os.path.join(ASSETS_DIR, "font2.ttf"), 20)
        small_font = ImageFont.truetype(os.path.join(ASSETS_DIR, "font2.ttf"), 16)
        tag_font = ImageFont.truetype(os.path.join(ASSETS_DIR, "font2.ttf"), 15)
        handle_font = ImageFont.truetype(os.path.join(ASSETS_DIR, "font.ttf"), 24)
    except OSError:
        title_font = meta_font = small_font = tag_font = handle_font = ImageFont.load_default()

    # NOW PLAYING tag (3D glassy)
    tag_x, tag_y = right_x, title_y - 48
    draw_now_playing_tag(bg, draw, tag_x, tag_y, tag_font)
    
    # bold‑look title
    nice_title = trim_to_width(title, title_font, MAX_TITLE_WIDTH)
    draw_smooth_bold_text(
        draw,
        (right_x, title_y),
        nice_title,
        title_font
    )

    # pink underline
    line_y = title_y + title_font.size + 6
    draw.line(
        [(right_x, line_y), (right_x + MAX_TITLE_WIDTH * 0.6, line_y)],
        fill=(255, 255, 255),
        width=3,
    )

    # meta text
    draw.text(
        (right_x, meta_y),
        f"Duration:  {duration}",
        fill=(255, 255, 255),
        font=meta_font,
    )
    draw.text(
        (right_x, meta_y + 32),
        f"Views:     {views}",
        fill=(255, 255, 255),
        font=meta_font,
    )

    # ============= THUMB.PNG OVERLAY (FIXED) =============
    PNG_OFFSET_X = 320
    PNG_OFFSET_Y = 85
    PNG_SCALE = 0.19
    PNG_OPACITY = 0.7

    try:
        # ✅ Updated to use absolute path via ASSETS_DIR
        overlay_path = os.path.join(ASSETS_DIR, "thumb.png")
        overlay_path = os.path.abspath(overlay_path)

        if os.path.exists(overlay_path):
            with Image.open(overlay_path).convert("RGBA") as overlay_img:
                # scale
                if PNG_SCALE != 1.0:
                    overlay_img = overlay_img.resize(
                        (int(overlay_img.width * PNG_SCALE),
                         int(overlay_img.height * PNG_SCALE)),
                        Image.Resampling.LANCZOS
                    )

                # opacity
                if PNG_OPACITY < 1.0:
                    alpha = overlay_img.split()[3]
                    alpha = alpha.point(lambda p: int(p * PNG_OPACITY))
                    overlay_img.putalpha(alpha)

                # position relative to panel
                x = panel_x + PNG_OFFSET_X
                y = panel_y + PNG_OFFSET_Y

                # ✅ STRICT PANEL CLIPPING
                crop_x1 = max(0, panel_x - x)
                crop_y1 = max(0, panel_y - y)
                crop_x2 = min(overlay_img.width, panel_x + PANEL_W - x)
                crop_y2 = min(overlay_img.height, panel_y + PANEL_H - y)

                if crop_x2 > crop_x1 and crop_y2 > crop_y1:
                    overlay_cropped = overlay_img.crop((crop_x1, crop_y1, crop_x2, crop_y2))
                    
                    paste_x = x + crop_x1
                    paste_y = y + crop_y1
                    
                    bg.paste(overlay_cropped, (paste_x, paste_y), overlay_cropped)

    except Exception:
        pass

    # progress bar
    grad_colors = random.choice(GRADIENT_SETS)
    bar_x = right_x
    filled = int(BAR_W * 0.6)

    for i in range(filled):
        rel = i / max(filled - 1, 1)
        seg = int(rel * (len(grad_colors) - 1))
        t = rel * (len(grad_colors) - 1) - seg
        c1 = grad_colors[seg]
        c2 = grad_colors[min(seg + 1, len(grad_colors) - 1)]
        col = (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t),
        )
        draw.line(
            [(bar_x + i, bar_y), (bar_x + i, bar_y + BAR_H)],
            fill=col,
            width=1,
        )

    draw.line(
        [(bar_x + filled, bar_y + BAR_H // 2),
         (bar_x + BAR_W, bar_y + BAR_H // 2)],
        fill=(255, 255, 255),
        width=BAR_H,
    )

    knob_x = bar_x + filled
    draw.ellipse(
        (knob_x - 7, bar_y - 4, knob_x + 7, bar_y + BAR_H + 4),
        fill=(255, 255, 255),
    )

    draw.text((bar_x, bar_y + 16), "00:00", fill="white", font=small_font)
    draw.text(
        (bar_x + BAR_W - 35, bar_y + 16),
        duration,
        fill="white",
        font=small_font,
    )

    # bottom meta
    bottom_text = f"{channel} | {views} | @BabiesIQ"
    draw.text(
        (thumb_x, thumb_y + THUMB_H + 18),
        bottom_text,
        fill=(240, 240, 240),
        font=small_font,
    )

    # user DP bottom‑right of card
    if user_id:
        dp = await download_and_process_profile_pic(user_id, USER_DP_SIZE)
        if dp:
            dp_3d = add_3d_dp_ring(dp, USER_DP_SIZE)

            bg.alpha_composite(
                dp_3d,
                (user_dp_x - 4, user_dp_y - 4)
            )

    # watermark
    draw.text(
        (CANVAS_W - 260, CANVAS_H - 40),
        "Powered by BabiesIQ",
        fill=(255, 255, 255),
        font=handle_font,
    )
    
    # ============= BABY.PNG OVERLAY (NEW) =============
    # yaha options set karo adjust karne ke liye
    BABY_ALIGN_X = "left"   # options: "left", "right"
    BABY_ALIGN_Y = "top"  # options: "top", "bottom"
    BABY_MARGIN_X = 30       # horizontal distance
    BABY_MARGIN_Y = 30       # vertical distance
    BABY_SCALE = 0.2         # size adjust
    BABY_BLEND = 0.6         # opacity/blend (0.0 to 1.0)

    try:
        baby_path = os.path.join(ASSETS_DIR, "baby.png")
        baby_path = os.path.abspath(baby_path)

        if os.path.exists(baby_path):
            with Image.open(baby_path).convert("RGBA") as baby_img:
                # scale
                if BABY_SCALE != 1.0:
                    baby_img = baby_img.resize(
                        (int(baby_img.width * BABY_SCALE),
                         int(baby_img.height * BABY_SCALE)),
                        Image.Resampling.LANCZOS
                    )

                # blend/opacity
                if BABY_BLEND < 1.0:
                    alpha = baby_img.split()[3]
                    alpha = alpha.point(lambda p: int(p * BABY_BLEND))
                    baby_img.putalpha(alpha)
                
                # left/right & top/bottom adjustments
                if BABY_ALIGN_X == "right":
                    bx = CANVAS_W - baby_img.width - BABY_MARGIN_X
                else:
                    bx = BABY_MARGIN_X
                    
                if BABY_ALIGN_Y == "bottom":
                    by = CANVAS_H - baby_img.height - BABY_MARGIN_Y
                else:
                    by = BABY_MARGIN_Y

                bg.paste(baby_img, (bx, by), baby_img)
    except Exception:
        pass


    # -------- GLOBAL NOISE OVERLAY --------
    if NOISE_IMG > 0:
        # bg RGBA hai, size leke grayscale noise banayenge
        w, h = bg.size
        # Pillow effect_noise se Gaussian noise texture
        noise_tex = Image.effect_noise((w, h), NOISE_IMG)

        # thoda blur karke soft grain jaisa
        noise_tex = noise_tex.filter(ImageFilter.GaussianBlur(0.5))

        # grayscale ko RGBA me convert with low alpha
        noise_rgba = Image.new("RGBA", (w, h))
        noise_rgba.putalpha(0)  # start fully transparent

        # grayscale ko 3‑channel me map + alpha set
        noise_arr = np.array(noise_tex, dtype="uint8")
        alpha_level = 40  # 0‑255, jitna zyada utna strong
        # simple way: use noise as alpha variation around alpha_level
        alpha = np.clip((noise_arr.astype("int16") - 128) // 4 + alpha_level,
                        0, 255).astype("uint8")
        rgba_arr = np.dstack([noise_arr, noise_arr, noise_arr, alpha])

        noise_rgba = Image.fromarray(rgba_arr, mode="RGBA")
        bg = Image.alpha_composite(bg, noise_rgba)  # overlay noise
    # --------------------------------------

    buffer = BytesIO()
    bg.convert("RGB").save(buffer, format="JPEG", quality=92)
    buffer.name = f"{videoid}.jpg"
    buffer.seek(0)

    return buffer
