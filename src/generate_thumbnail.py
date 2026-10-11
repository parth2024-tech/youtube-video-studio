#!/usr/bin/env python3
"""
Thumbnail Generator for Autonomous YouTube Studio
Creates a high-contrast, mobile-optimized 1280x720 thumbnail.
Strictly complies with Rule #1 & #2:
- Replaces "$234B SAAS SHIFT" with "$234B AT RISK".
- Removes "killing", "dismantling", and "death" framing.
- Uses "Gartner estimate" and "up to $234B".
- Readable down to 320px width on mobile feeds using textbbox.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def render_thumbnail(output_path="output/saaspocalypse-ai-agents/thumbnail.png"):
    width, height = 1280, 720
    img = Image.new("RGB", (width, height), color="#080c14")
    draw = ImageDraw.Draw(img)

    # Gradient background
    for y in range(height):
        r = int(8 + (y / height) * 12)
        g = int(12 + (y / height) * 16)
        b = int(20 + (y / height) * 30)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Load high-contrast fonts
    font_paths = [
        "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Bold.ttf",
        "/usr/share/fonts/noto/NotoSans-Bold.ttf"
    ]
    font_path = None
    for p in font_paths:
        if os.path.exists(p):
            font_path = p
            break

    if font_path:
        font_hero = ImageFont.truetype(font_path, 92)
        font_badge = ImageFont.truetype(font_path, 32)
        font_card_lg = ImageFont.truetype(font_path, 48)
        font_card_sm = ImageFont.truetype(font_path, 28)
    else:
        font_hero = font_badge = font_card_lg = font_card_sm = ImageFont.load_default()

    # 1. Top Badge: "Gartner estimate"
    badge_text = "Gartner estimate"
    bbox_b = draw.textbbox((0, 0), badge_text, font=font_badge)
    bw = bbox_b[2] - bbox_b[0]
    bh = bbox_b[3] - bbox_b[1]
    bx0, by0 = (width - bw) // 2 - 24, 30
    bx1, by1 = bx0 + bw + 48, by0 + bh + 24
    draw.rounded_rectangle([(bx0, by0), (bx1, by1)], radius=12, fill="#e11d48")
    draw.text((bx0 + 24, by0 + 8), badge_text, fill="#ffffff", font=font_badge)

    # 2. Main Center Hook: 3 LARGE WORDS ("THE $234B AT RISK")
    # Perfectly readable at 320px wide!
    line1 = "UP TO $234B"
    line2 = "AT RISK"

    bbox_l1 = draw.textbbox((0, 0), line1, font=font_hero)
    w_l1 = bbox_l1[2] - bbox_l1[0]
    x_l1 = (width - w_l1) // 2
    y_l1 = 100

    bbox_l2 = draw.textbbox((0, 0), line2, font=font_hero)
    w_l2 = bbox_l2[2] - bbox_l2[0]
    x_l2 = (width - w_l2) // 2
    y_l2 = 195

    # Text shadow for maximum contrast
    draw.text((x_l1 + 4, y_l1 + 4), line1, fill="#000000", font=font_hero)
    draw.text((x_l1, y_l1), line1, fill="#ffffff", font=font_hero)

    draw.text((x_l2 + 4, y_l2 + 4), line2, fill="#000000", font=font_hero)
    draw.text((x_l2, y_l2), line2, fill="#38bdf8", font=font_hero)

    # 3. Two Comparison Cards (Legacy Seat vs AI Agent API)
    # Left Card
    c1_x0, c1_y0, c1_x1, c1_y1 = 80, 320, 600, 650
    draw.rounded_rectangle([(c1_x0, c1_y0), (c1_x1, c1_y1)], radius=20, fill="#131b2e", outline="#ef4444", width=3)
    
    label_old = "OLD: PER-SEAT SaaS"
    draw.text((c1_x0 + 35, c1_y0 + 30), label_old, fill="#f87171", font=font_card_sm)

    seat_price = "$120 / MO"
    draw.text((c1_x0 + 35, c1_y0 + 90), seat_price, fill="#ffffff", font=font_card_lg)
    # Red strike-through line
    draw.line([(c1_x0 + 30, c1_y0 + 120), (c1_x0 + 320, c1_y0 + 120)], fill="#ef4444", width=8)

    sub_old = "Per Human Login"
    draw.text((c1_x0 + 35, c1_y0 + 170), sub_old, fill="#94a3b8", font=font_card_sm)
    sub_old2 = "Manual Dashboard"
    draw.text((c1_x0 + 35, c1_y0 + 220), sub_old2, fill="#64748b", font=font_card_sm)

    # Right Card
    c2_x0, c2_y0, c2_x1, c2_y1 = 680, 320, 1200, 650
    draw.rounded_rectangle([(c2_x0, c2_y0), (c2_x1, c2_y1)], radius=20, fill="#0b1e36", outline="#00e5ff", width=3)

    label_new = "NEW: AI AGENT API"
    draw.text((c2_x0 + 35, c2_y0 + 30), label_new, fill="#00e5ff", font=font_card_sm)

    agent_price = "NO SEATS"
    draw.text((c2_x0 + 35, c2_y0 + 90), agent_price, fill="#38bdf8", font=font_card_lg)

    sub_new = "Direct API Workflows"
    draw.text((c2_x0 + 35, c2_y0 + 170), sub_new, fill="#e2e8f0", font=font_card_sm)
    sub_new2 = "Outcome-Based Value"
    draw.text((c2_x0 + 35, c2_y0 + 220), sub_new2, fill="#4ade80", font=font_card_sm)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"Thumbnail rendered successfully to {output_path}")

    # Also save 320px version
    thumb320 = img.resize((320, 180), Image.Resampling.LANCZOS)
    thumb320.save("output/saaspocalypse-ai-agents/thumbnail_320px.png")
    print("Saved 320px version to output/saaspocalypse-ai-agents/thumbnail_320px.png")

if __name__ == "__main__":
    render_thumbnail()
