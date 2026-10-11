#!/usr/bin/env python3
"""
Thumbnail Generator for Autonomous YouTube Studio
Creates a high-contrast, mobile-optimized 1280x720 thumbnail.
Readable down to 320px width on mobile feeds.
Uses Pillow with textbbox for exact text bounds measurement.
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
        font_hero = ImageFont.truetype(font_path, 88)
        font_badge = ImageFont.truetype(font_path, 32)
        font_card_lg = ImageFont.truetype(font_path, 48)
        font_card_sm = ImageFont.truetype(font_path, 28)
    else:
        font_hero = font_badge = font_card_lg = font_card_sm = ImageFont.load_default()

    # 1. Top Badge: "Gartner estimate" (Mandated change)
    badge_text = "Gartner estimate"
    bbox_b = draw.textbbox((0, 0), badge_text, font=font_badge)
    bw = bbox_b[2] - bbox_b[0]
    bh = bbox_b[3] - bbox_b[1]
    bx0, by0 = (width - bw) // 2 - 24, 30
    bx1, by1 = bx0 + bw + 48, by0 + bh + 24
    draw.rounded_rectangle([(bx0, by0), (bx1, by1)], radius=12, fill="#e11d48")
    draw.text((bx0 + 24, by0 + 8), badge_text, fill="#ffffff", font=font_badge)

    # 2. Main Center Hook: 4 LARGE WORDS (Readable at 320px wide)
    # Text: "THE $234B SAAS SHIFT"
    line1 = "THE $234B"
    line2 = "SAAS SHIFT"

    bbox_l1 = draw.textbbox((0, 0), line1, font=font_hero)
    w_l1 = bbox_l1[2] - bbox_l1[0]
    x_l1 = (width - w_l1) // 2
    y_l1 = 100

    bbox_l2 = draw.textbbox((0, 0), line2, font=font_hero)
    w_l2 = bbox_l2[2] - bbox_l2[0]
    x_l2 = (width - w_l2) // 2
    y_l2 = 195

    # Text shadow for high contrast pop
    draw.text((x_l1 + 4, y_l1 + 4), line1, fill="#000000", font=font_hero)
    draw.text((x_l1, y_l1), line1, fill="#ffffff", font=font_hero)

    draw.text((x_l2 + 4, y_l2 + 4), line2, fill="#000000", font=font_hero)
    draw.text((x_l2, y_l2), line2, fill="#38bdf8", font=font_hero)

    # 3. Two Comparison Cards (Left: Dead Seat License / Right: AI Agent API)
    # Left Card (Legacy Seat)
    c1_x0, c1_y0, c1_x1, c1_y1 = 80, 320, 600, 650
    draw.rounded_rectangle([(c1_x0, c1_y0), (c1_x1, c1_y1)], radius=20, fill="#131b2e", outline="#ef4444", width=3)
    
    label_old = "OLD: SEAT LICENSE"
    draw.text((c1_x0 + 35, c1_y0 + 30), label_old, fill="#f87171", font=font_card_sm)

    seat_price = "$120 / MO"
    draw.text((c1_x0 + 35, c1_y0 + 90), seat_price, fill="#ffffff", font=font_card_lg)
    # Bold red strike-through across $120/MO
    draw.line([(c1_x0 + 30, c1_y0 + 120), (c1_x0 + 320, c1_y0 + 120)], fill="#ef4444", width=8)

    sub_old = "Per Human Login"
    draw.text((c1_x0 + 35, c1_y0 + 170), sub_old, fill="#94a3b8", font=font_card_sm)
    sub_old2 = "Manual Dashboard"
    draw.text((c1_x0 + 35, c1_y0 + 220), sub_old2, fill="#64748b", font=font_card_sm)

    # Right Card (AI Agent API)
    c2_x0, c2_y0, c2_x1, c2_y1 = 680, 320, 1200, 650
    draw.rounded_rectangle([(c2_x0, c2_y0), (c2_x1, c2_y1)], radius=20, fill="#0b1e36", outline="#00e5ff", width=3)

    label_new = "NEW: AI AGENT API"
    draw.text((c2_x0 + 35, c2_y0 + 30), label_new, fill="#00e5ff", font=font_card_sm)

    agent_price = "NO SEATS"
    draw.text((c2_x0 + 35, c2_y0 + 90), agent_price, fill="#38bdf8", font=font_card_lg)

    sub_new = "Direct API Calls"
    draw.text((c2_x0 + 35, c2_y0 + 170), sub_new, fill="#e2e8f0", font=font_card_sm)
    sub_new2 = "Zero GUI Overhead"
    draw.text((c2_x0 + 35, c2_y0 + 220), sub_new2, fill="#4ade80", font=font_card_sm)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"Thumbnail rendered successfully to {output_path}")

if __name__ == "__main__":
    render_thumbnail()
