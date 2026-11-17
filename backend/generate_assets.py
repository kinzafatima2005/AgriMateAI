"""
AgriMate AI - Asset Generator
Generates high-resolution branded logo and sample imagery for the Flutter app.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFilter

ASSETS_DIR = r"c:\Users\SMART TECH\Desktop\AgriMateAI\frontend\assets"
os.makedirs(ASSETS_DIR, exist_ok=True)


def create_logo():
    """Generates crisp 512x512 AgriMate emblem with olive green shield, golden yellow sprout and leaf."""
    size = (512, 512)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    olive_bg = (107, 138, 71, 255)       # #6B8A47
    lime_yellow = (244, 242, 58, 255)    # #F4F23A
    dark_olive = (61, 82, 38, 255)       # #3D5226
    white = (255, 255, 255, 255)

    # Circular badge
    draw.ellipse([32, 32, 480, 480], fill=olive_bg, outline=lime_yellow, width=8)

    # Stylized Sprout / Leaf icon
    # Left leaf
    draw.pieslice([160, 140, 320, 360], start=180, end=300, fill=lime_yellow)
    draw.pieslice([200, 160, 360, 380], start=240, end=360, fill=white)
    
    # Stem
    draw.arc([180, 200, 340, 420], start=30, end=150, fill=lime_yellow, width=12)

    # Grain dots
    for i, offset in enumerate([(220, 150), (256, 120), (292, 150)]):
        draw.ellipse([offset[0]-10, offset[1]-10, offset[0]+10, offset[1]+10], fill=lime_yellow)

    # Inner circular ring
    draw.ellipse([64, 64, 448, 448], outline=(255, 255, 255, 50), width=4)

    path = os.path.join(ASSETS_DIR, "logo.png")
    img.save(path, "PNG")
    print(f"Generated logo at {path}")


def create_farmer_character():
    """Generates a friendly stylized 3D farmer character holding wheat."""
    size = (600, 700)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Soft glowing background circle
    draw.ellipse([100, 150, 500, 550], fill=(244, 242, 58, 40))

    # Body / Overalls (olive green & denim)
    draw.ellipse([160, 380, 440, 700], fill=(61, 82, 38, 255))
    draw.rectangle([210, 420, 390, 700], fill=(85, 115, 55, 255))

    # Head / Face
    draw.ellipse([210, 200, 390, 380], fill=(245, 200, 160, 255))
    
    # Cheerful Eyes & Smile
    draw.arc([250, 260, 280, 290], start=0, end=180, fill=(40, 50, 30, 255), width=4)
    draw.arc([320, 260, 350, 290], start=0, end=180, fill=(40, 50, 30, 255), width=4)
    draw.arc([270, 300, 330, 340], start=0, end=180, fill=(180, 70, 70, 255), width=5)

    # Friendly White Mustache
    draw.chord([260, 305, 340, 325], start=0, end=180, fill=(245, 245, 245, 255))

    # Straw Hat (Golden Yellow)
    draw.ellipse([130, 160, 470, 240], fill=(230, 195, 75, 255), outline=(190, 155, 45, 255), width=4)
    draw.pieslice([190, 90, 410, 220], start=180, end=360, fill=(244, 210, 85, 255))
    draw.rectangle([200, 175, 400, 195], fill=(180, 60, 50, 255)) # Hat band

    # Wheat Stalks in hand
    stalk_color = (244, 242, 58, 255)
    for angle, x, y in [(-20, 410, 280), (0, 430, 270), (20, 450, 280)]:
        draw.line([(380, 450), (x, y)], fill=(200, 170, 40, 255), width=6)
        for wy in range(y, y + 100, 20):
            draw.ellipse([x - 12, wy, x + 12, wy + 16], fill=stalk_color)

    path = os.path.join(ASSETS_DIR, "farmer_3d.png")
    img.save(path, "PNG")
    print(f"Generated farmer character at {path}")


def create_farmland_photos():
    """Generates lush organic drone-view aerial farmland images."""
    size = (800, 500)
    img = Image.new("RGB", size, (90, 125, 60))
    draw = ImageDraw.Draw(img)

    # Geometric crop fields (typical aerial drone view)
    fields = [
        ([0, 0, 380, 240], (115, 150, 75)),
        ([380, 0, 800, 220], (95, 130, 60)),
        ([0, 240, 450, 500], (80, 115, 50)),
        ([450, 220, 800, 500], (130, 165, 85)),
        ([150, 80, 320, 200], (145, 180, 95)),
    ]
    for bbox, col in fields:
        draw.rectangle(bbox, fill=col)

    # Irrigation canals and tractor lines
    draw.line([(0, 240), (800, 220)], fill=(70, 100, 120), width=6) # Canal
    draw.line([(450, 0), (450, 500)], fill=(160, 140, 110), width=8) # Farm road

    for y in range(20, 220, 15):
        draw.line([(20, y), (360, y)], fill=(105, 140, 70), width=2)
    for x in range(470, 780, 20):
        draw.line([(x, 240), (x, 480)], fill=(120, 155, 75), width=2)

    img = img.filter(ImageFilter.GaussianBlur(1))

    path = os.path.join(ASSETS_DIR, "field_aerial.jpg")
    img.save(path, "JPEG", quality=90)
    
    # Header panoramic
    hdr = img.crop((0, 0, 800, 420)).resize((1000, 600))
    hdr_path = os.path.join(ASSETS_DIR, "field_aerial_header.jpg")
    hdr.save(hdr_path, "JPEG", quality=92)
    print(f"Generated farmland drone textures at {path} and {hdr_path}")


if __name__ == "__main__":
    create_logo()
    create_farmer_character()
    create_farmland_photos()

