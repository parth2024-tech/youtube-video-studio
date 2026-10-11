#!/usr/bin/env python3
"""
Kids Story Visual Generator
Creates vibrant, storybook-style vertical 1080x1920 slides for Kids Bedtime Fables.
Features friendly color themes, warm storybook framing, and child-safe visual design.
"""

import os
from PIL import Image, ImageDraw, ImageFont

FRAMES_DIR = "output/kids-bedtime-fables/render_frames"
os.makedirs(FRAMES_DIR, exist_ok=True)

FONT_PATH = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"

def make_kids_slide(filename, bg_colors, header_emoji, title, story_box_color, main_text, moral_text=None):
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    # Soft vertical gradient background
    c_top, c_bottom = bg_colors
    for y in range(height):
        factor = y / height
        r = int(c_top[0] + factor * (c_bottom[0] - c_top[0]))
        g = int(c_top[1] + factor * (c_bottom[1] - c_top[1]))
        b = int(c_top[2] + factor * (c_bottom[2] - c_top[2]))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    f_title = ImageFont.truetype(FONT_PATH, 58)
    f_sub = ImageFont.truetype(FONT_PATH, 38)
    f_body = ImageFont.truetype(FONT_PATH, 34)
    f_moral = ImageFont.truetype(FONT_PATH, 32)

    # Decorative header card
    draw.rounded_rectangle([(80, 120), (1000, 260)], radius=30, fill="#ffffff", outline="#fcd34d", width=4)
    draw.text((120, 160), title, fill="#1e293b", font=f_title)

    # Main Storybook Illustration Card
    draw.rounded_rectangle([(70, 310), (1010, 1550)], radius=36, fill=story_box_color, outline="#ffffff", width=4)

    # Center Narrative Text Card
    draw.rounded_rectangle([(110, 750), (970, 1480)], radius=28, fill="#ffffff", outline="#e2e8f0", width=2)

    # Word wrap main story text
    words = main_text.split()
    lines = []
    cur = []
    for w in words:
        cur.append(w)
        if len(" ".join(cur)) > 32:
            lines.append(" ".join(cur))
            cur = []
    if cur:
        lines.append(" ".join(cur))

    y_t = 820
    for l in lines:
        draw.text((150, y_t), l, fill="#1e293b", font=f_body)
        y_t += 62

    # Bottom Moral Card
    if moral_text:
        draw.rounded_rectangle([(90, 1600), (990, 1800)], radius=24, fill="#ffffff", outline="#38bdf8", width=3)
        draw.text((130, 1640), "✨ GENTLE LESSON ✨", fill="#0284c7", font=f_moral)
        draw.text((130, 1700), moral_text, fill="#334155", font=f_moral)

    path = os.path.join(FRAMES_DIR, filename)
    img.save(path, quality=95)
    print(f"Generated {path}")

def generate_all_kids_slides():
    print("Generating story slides...")
    
    # --- Short 1: Barnaby the Bear (Forest Green & Honey Yellow theme) ---
    make_kids_slide(
        "short1_01.png",
        bg_colors=((24, 75, 45), (10, 35, 20)),
        header_emoji="🐻",
        title="Barnaby Lost His Roar!",
        story_box_color="#fef3c7",
        main_text="One sunny morning in Whispering Woods, Barnaby the Bear woke up and his mighty roar was gone! Instead of a big roar, only a tiny squeak came out.",
        moral_text="Even big bears have quiet days."
    )
    make_kids_slide(
        "short1_02.png",
        bg_colors=((30, 85, 55), (15, 45, 25)),
        header_emoji="🐰",
        title="A Tiny Lost Friend",
        story_box_color="#fef9c3",
        main_text="Barnaby found a tiny lost bunny shivering in the tall grass. He spoke with his soft, gentle whisper. The bunny giggled and hopped right onto his shoulder!",
        moral_text="Kind words are the bravest words."
    )
    make_kids_slide(
        "short1_03.png",
        bg_colors=((20, 60, 40), (8, 25, 15)),
        header_emoji="🌙",
        title="Sweet Dreams, Little Bear",
        story_box_color="#ecfdf5",
        main_text="Barnaby smiled. He didn't need to be loud to help his friends. Gentle kindness was the greatest superpower of all.",
        moral_text="Sweet dreams, little one."
    )

    # --- Short 2: Pip the Little Cloud (Sky Blue & Rainbow theme) ---
    make_kids_slide(
        "short2_01.png",
        bg_colors=((14, 116, 144), (7, 50, 70)),
        header_emoji="☁️",
        title="Pip's Big Rainbow Dream",
        story_box_color="#e0f2fe",
        main_text="High in the sky, Pip the little cloud wanted to make a rainbow all by himself. He puffed his cheeks and rained, but only made a gray puddle.",
        moral_text="It's okay to ask for a helping hand."
    )
    make_kids_slide(
        "short2_02.png",
        bg_colors=((2, 132, 199), (3, 70, 110)),
        header_emoji="☀️",
        title="Sunny Lent a Golden Ray!",
        story_box_color="#fef08a",
        main_text="Sunny the golden sun peeked out: 'You have raindrops, Pip, and I have golden light. Let's make magic together!' Sunny shone through the droplets...",
        moral_text="Teamwork makes colors bright."
    )
    make_kids_slide(
        "short2_03.png",
        bg_colors=((3, 105, 161), (12, 40, 75)),
        header_emoji="🌈",
        title="A Sky Full of Rainbows!",
        story_box_color="#fdf4ff",
        main_text="Suddenly, a breathtaking rainbow painted the entire sky from cloud to cloud! Together, their friendship created wonder.",
        moral_text="Sleep tight, sweet dreamer."
    )

    # --- Short 3: Oliver the Owl (Night Sky Navy & Star Gold theme) ---
    make_kids_slide(
        "short3_01.png",
        bg_colors=((15, 23, 42), (30, 27, 75)),
        header_emoji="🦉",
        title="Oliver & the Night Sky",
        story_box_color="#e0e7ff",
        main_text="Oliver the baby owl lived in a cozy tree hollow. But Oliver was afraid of the dark! When the sun set, he hid under his soft wings.",
        moral_text="Being afraid is where bravery begins."
    )
    make_kids_slide(
        "short3_02.png",
        bg_colors=((30, 27, 75), (49, 46, 129)),
        header_emoji="✨",
        title="Lumina's Sparkly Secret",
        story_box_color="#fae8ff",
        main_text="A little firefly named Lumina whispered: 'Oliver, peek outside! The dark is just the blanket that lets the sparkly stars come out to play!'",
        moral_text="Look closely, and you'll find magic."
    )
    make_kids_slide(
        "short3_03.png",
        bg_colors=((15, 23, 42), (2, 6, 23)),
        header_emoji="⭐",
        title="The Stars Are Watching",
        story_box_color="#ede9fe",
        main_text="Oliver opened his big golden eyes. The forest glowed with moonlight and shooting stars. It wasn't scary at all; it was wondrous.",
        moral_text="Close your eyes, little explorer."
    )

if __name__ == "__main__":
    generate_all_kids_slides()
