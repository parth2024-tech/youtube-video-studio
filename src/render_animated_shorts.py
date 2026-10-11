#!/usr/bin/env python3
"""
High-End 30 FPS Animation Engine for YouTube Shorts (Kids Bedtime Fables)
Features:
- Full continuous 30fps animation (No static slides!)
- 6-axis smooth cinematic camera choreography (Ken Burns zoom, pan, tilt, breathe)
- Multi-layer procedural dynamic particle systems:
    * Barnaby: 50 swirling golden dust motes + 16 tumbling swaying leaves + bunny aura
    * Pip: Dynamic cascading rain & ripple splashes -> rotating sunbeams -> shimmering rainbow sparkle burst
    * Oliver: 70 pulsing stars + 4 high-speed shooting stars + Lumina the firefly flying in organic 3D orbit with stardust trail
- Kinetic bouncy subtitle badges with spring pop-in animations
- Direct high-speed raw RGB pipe into FFmpeg (zero intermediate image disk writes)
"""

import os
import math
import random
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "output/kids-bedtime-fables"
ASSETS_DIR = "output/kids-bedtime-fables/assets"
FONT_PATH = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"

WIDTH, HEIGHT = 1080, 1920
FPS = 30

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

# -------------------------------------------------------------
# ANIMATION SUBSYSTEM: BARNABY THE BEAR
# -------------------------------------------------------------
def render_barnaby_short(output_path, audio_path, duration=40.18):
    print(f"--- Rendering Animated Short #1: Barnaby the Bear ({duration}s @ {FPS}fps) ---")
    base_img = Image.open(os.path.join(ASSETS_DIR, "barnaby.jpg")).convert("RGBA")
    # Upscale base image so camera has generous margins to pan and zoom
    UP_W, UP_H = 1512, 2688
    base_large = base_img.resize((UP_W, UP_H), Image.Resampling.LANCZOS)

    captions = [
        (0.0, 6.5, "One sunny morning in Whispering Woods, Barnaby the Bear woke up..."),
        (6.5, 13.0, "And his mighty roar was gone! All that came out was a tiny squeak."),
        (13.0, 19.5, "Barnaby felt embarrassed. How could he be brave without a loud voice?"),
        (19.5, 26.0, "On his quiet walk, he found a tiny lost bunny in the tall grass."),
        (26.0, 33.5, "Barnaby spoke so gently that the bunny giggled and hopped onto his shoulder!"),
        (33.5, duration, "He smiled. Being kind and gentle is the bravest thing of all. Sweet dreams! ✨")
    ]

    # Initialize Particle Systems
    random.seed(42)
    # 50 Golden Dust Motes
    dust_motes = [
        {
            "x": random.uniform(50, WIDTH - 50),
            "y": random.uniform(100, HEIGHT - 300),
            "vx": random.uniform(-25, 25),
            "vy": random.uniform(-40, -10),
            "radius": random.uniform(3, 7),
            "phase": random.uniform(0, math.pi * 2),
            "freq": random.uniform(1.5, 3.5)
        }
        for _ in range(50)
    ]

    # 18 Falling Autumn Leaves
    leaf_colors = [(235, 150, 40, 210), (220, 110, 30, 200), (240, 180, 50, 220), (180, 130, 45, 190)]
    leaves = [
        {
            "x": random.uniform(50, WIDTH - 50),
            "y": random.uniform(-HEIGHT, HEIGHT),
            "vy": random.uniform(70, 130),
            "sway_amp": random.uniform(40, 90),
            "sway_freq": random.uniform(1.2, 2.5),
            "rot_speed": random.uniform(1.5, 3.5),
            "size": random.uniform(14, 24),
            "color": random.choice(leaf_colors),
            "phase": random.uniform(0, math.pi * 2)
        }
        for _ in range(18)
    ]

    total_frames = int(duration * FPS)

    # Launch FFmpeg pipe
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgba",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-r", str(FPS),
        "-i", "-",
        "-i", audio_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_path
    ]
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    font_sub = get_font(38)

    for f_idx in range(total_frames):
        t = f_idx / FPS

        # 1. Camera Choreography (Ken Burns: Multi-phase zoom & tilt)
        # Phase 1: 0-13s: Gentle push in towards Barnaby
        # Phase 2: 13-26s: Slow drift down towards bunny
        # Phase 3: 26-40s: Breathing zoom into Barnaby & bunny together
        progress = t / duration
        zoom = 1.08 + 0.08 * math.sin(progress * math.pi) + 0.015 * math.sin(t * 1.5)
        # Pan coordinates on base_large
        center_x = UP_W * (0.50 + 0.04 * math.sin(t * 0.4))
        center_y = UP_H * (0.48 + 0.05 * math.sin(t * 0.35 + 0.5))

        crop_w = int(WIDTH / zoom)
        crop_h = int(HEIGHT / zoom)
        x0 = max(0, min(UP_W - crop_w, int(center_x - crop_w / 2)))
        y0 = max(0, min(UP_H - crop_h, int(center_y - crop_h / 2)))

        frame_crop = base_large.crop((x0, y0, x0 + crop_w, y0 + crop_h))
        frame = frame_crop.resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)

        # Dynamic overlay canvas
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)

        # 2. Render Animated Sunbeam Dust Motes
        for mote in dust_motes:
            # Physics update
            mx = (mote["x"] + mote["vx"] * (1 / FPS) + 30 * math.sin(t * 1.8 + mote["phase"])) % WIDTH
            my = (mote["y"] + mote["vy"] * (1 / FPS)) % (HEIGHT - 250)
            mote["x"], mote["y"] = mx, my
            # Alpha pulsation
            alpha = int(120 + 110 * math.sin(t * mote["freq"] + mote["phase"]))
            r = mote["radius"] + 1.5 * math.sin(t * 3.0 + mote["phase"])
            # Draw glowing halo + core
            draw_ov.ellipse([mx - r * 2.2, my - r * 2.2, mx + r * 2.2, my + r * 2.2], fill=(255, 230, 140, int(alpha * 0.35)))
            draw_ov.ellipse([mx - r, my - r, mx + r, my + r], fill=(255, 255, 210, alpha))

        # 3. Render Animated Falling & Tumbling Leaves
        for leaf in leaves:
            leaf["y"] += leaf["vy"] * (1 / FPS)
            if leaf["y"] > HEIGHT + 40:
                leaf["y"] = -40
                leaf["x"] = random.uniform(50, WIDTH - 50)
            lx = leaf["x"] + leaf["sway_amp"] * math.sin(t * leaf["sway_freq"] + leaf["phase"])
            ly = leaf["y"]
            rot = t * leaf["rot_speed"] + leaf["phase"]
            sz = leaf["size"]
            # Draw rotated leaf diamond
            c, s = math.cos(rot), math.sin(rot)
            pts = [
                (lx + sz * c, ly + sz * s),
                (lx - sz * 0.4 * s, ly + sz * 0.4 * c),
                (lx - sz * 0.8 * c, ly - sz * 0.8 * s),
                (lx + sz * 0.4 * s, ly - sz * 0.4 * c),
            ]
            draw_ov.polygon(pts, fill=leaf["color"])

        # 4. Magical Bunny & Bear Heartbeat Aura (pulsing golden halo around character interaction)
        aura_r = 170 + 25 * math.sin(t * 3.0)
        aura_alpha = int(35 + 25 * math.sin(t * 2.5))
        bx, by = int(WIDTH * 0.68), int(HEIGHT * 0.48)
        draw_ov.ellipse([bx - aura_r, by - aura_r, bx + aura_r, by + aura_r], outline=(255, 235, 130, aura_alpha), width=6)

        # 5. Kinetic Subtitle Badge
        active_sub = None
        for s_start, s_end, txt in captions:
            if s_start <= t < s_end:
                active_sub = (s_start, s_end, txt)
                break

        if active_sub:
            s_start, s_end, text = active_sub
            dt = t - s_start
            # Pop-in spring bounce
            scale = 1.0 if dt > 0.35 else min(1.0, 0.75 + 0.3 * math.sin(dt / 0.35 * math.pi * 1.5))

            box_w = int(960 * scale)
            box_h = 160
            box_x = (WIDTH - box_w) // 2
            box_y = HEIGHT - 270

            # Subtitle Frosted Badge
            draw_ov.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=28, fill=(12, 22, 16, 215), outline=(255, 215, 100, 230), width=4)
            lines = wrap_text(text, font_sub, box_w - 60, draw_ov)
            total_text_h = len(lines) * 48
            start_ty = box_y + (box_h - total_text_h) // 2
            for i, line in enumerate(lines):
                line_bbox = draw_ov.textbbox((0, 0), line, font=font_sub)
                lw = line_bbox[2] - line_bbox[0]
                tx = box_x + (box_w - lw) // 2
                ty = start_ty + i * 48
                # Drop shadow
                draw_ov.text((tx + 2, ty + 2), line, font=font_sub, fill=(0, 0, 0, 230))
                # Text fill (gold-yellow highlight for last words, white for body)
                draw_ov.text((tx, ty), line, font=font_sub, fill=(255, 255, 245, 255))

        # Composite frame
        final_frame = Image.alpha_composite(frame, overlay)
        proc.stdin.write(final_frame.tobytes())

        if f_idx % (FPS * 5) == 0:
            print(f"  Barnaby: {f_idx}/{total_frames} frames rendered ({t:.1f}s)...")

    proc.stdin.close()
    proc.wait()
    print(f"Short #1 successfully rendered: {output_path}")

# -------------------------------------------------------------
# ANIMATION SUBSYSTEM: PIP THE CLOUD AND THE RAINBOW
# -------------------------------------------------------------
def render_pip_short(output_path, audio_path, duration=40.46):
    print(f"--- Rendering Animated Short #2: Pip the Cloud ({duration}s @ {FPS}fps) ---")
    base_img = Image.open(os.path.join(ASSETS_DIR, "pip.jpg")).convert("RGBA")
    UP_W, UP_H = 1512, 2688
    base_large = base_img.resize((UP_W, UP_H), Image.Resampling.LANCZOS)

    captions = [
        (0.0, 6.5, "High in the sky, Pip the little cloud wanted to make a rainbow all by himself."),
        (6.5, 13.5, "Pip puffed his cheeks and rained and rained... but only made a gray puddle."),
        (13.5, 20.0, "He felt sad and sighed. Then, Sunny the golden sun peeked out with a warm smile!"),
        (20.0, 26.5, "'You have raindrops, Pip, and I have golden light. Let's make magic together!'"),
        (26.5, 33.5, "Sunny shone through Pip's raindrops, and a bright rainbow painted the sky! 🌈"),
        (33.5, duration, "Pip laughed with joy. Together, they made magic. Sleep tight, sweet dreamer! ☁️✨")
    ]

    total_frames = int(duration * FPS)

    # Particle systems: Raindrops & Splash Ripples
    random.seed(101)
    raindrops = [
        {
            "x": random.uniform(30, WIDTH - 30),
            "y": random.uniform(-HEIGHT, HEIGHT),
            "speed": random.uniform(950, 1500),
            "length": random.uniform(25, 45),
            "alpha": random.randint(140, 220)
        }
        for _ in range(85)
    ]
    splashes = []

    # Rainbow sparkles
    sparkles = [
        {
            "x": random.uniform(100, WIDTH - 100),
            "y": random.uniform(280, 720),
            "vx": random.uniform(-20, 20),
            "vy": random.uniform(-15, 25),
            "radius": random.uniform(4, 9),
            "phase": random.uniform(0, math.pi * 2),
            "color": random.choice([(255, 230, 100), (255, 130, 180), (120, 225, 255), (180, 255, 130)])
        }
        for _ in range(50)
    ]

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgba",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-r", str(FPS),
        "-i", "-",
        "-i", audio_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_path
    ]
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    font_sub = get_font(38)

    for f_idx in range(total_frames):
        t = f_idx / FPS

        # Camera choreography:
        # 0-14s: focus top-left on Pip raining
        # 14-27s: pan right to Sunny
        # 27-40s: wide panoramic pullback celebrating rainbow
        if t < 14.0:
            pan_x_pct = 0.42 + 0.03 * math.sin(t * 0.5)
            pan_y_pct = 0.38 + 0.02 * math.sin(t * 0.4)
            zoom = 1.15 + 0.04 * math.sin(t * 0.8)
        elif t < 27.0:
            p = (t - 14.0) / 13.0
            pan_x_pct = 0.42 + 0.16 * p
            pan_y_pct = 0.38 + 0.02 * math.sin(t * 0.5)
            zoom = 1.15 - 0.05 * p
        else:
            p = (t - 27.0) / (duration - 27.0)
            pan_x_pct = 0.50 + 0.02 * math.sin(t * 0.4)
            pan_y_pct = 0.45 - 0.05 * p
            zoom = 1.08 + 0.04 * math.sin(t * 0.6)

        crop_w = int(WIDTH / zoom)
        crop_h = int(HEIGHT / zoom)
        x0 = max(0, min(UP_W - crop_w, int(UP_W * pan_x_pct - crop_w / 2)))
        y0 = max(0, min(UP_H - crop_h, int(UP_H * pan_y_pct - crop_h / 2)))

        frame_crop = base_large.crop((x0, y0, x0 + crop_w, y0 + crop_h))
        frame = frame_crop.resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)

        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)

        # Effect 1: Rain Animation (Active heavily during 0s - 14s, fades out by 20s)
        rain_intensity = 1.0 if t < 14.0 else max(0.0, 1.0 - (t - 14.0) / 6.0)
        if rain_intensity > 0.01:
            for drop in raindrops:
                drop["y"] += drop["speed"] * (1 / FPS)
                if drop["y"] > HEIGHT - 350:
                    # Trigger splash ripple
                    if random.random() < 0.3:
                        splashes.append({"x": drop["x"], "y": drop["y"], "r": 2.0, "life": 0.25})
                    drop["y"] = random.uniform(-100, 0)
                    drop["x"] = random.uniform(30, WIDTH - 30)

                # Draw angled dynamic raindrop streak
                alpha = int(drop["alpha"] * rain_intensity)
                dx, dy = 4, drop["length"]
                draw_ov.line([(drop["x"], drop["y"]), (drop["x"] + dx, drop["y"] + dy)], fill=(180, 220, 255, alpha), width=3)

            # Update and draw splash ripples
            new_splashes = []
            for s in splashes:
                s["r"] += 35 * (1 / FPS)
                s["life"] -= (1 / FPS)
                if s["life"] > 0:
                    sa = int(180 * (s["life"] / 0.25) * rain_intensity)
                    rx, ry = s["r"] * 1.8, s["r"] * 0.7
                    draw_ov.ellipse([s["x"] - rx, s["y"] - ry, s["x"] + rx, s["y"] + ry], outline=(200, 235, 255, sa), width=2)
                    new_splashes.append(s)
            splashes = new_splashes

        # Effect 2: Rotating Sunbeams around Sunny (Active from 14s onward)
        if t >= 13.5:
            sun_intensity = min(1.0, (t - 13.5) / 4.0)
            sun_center = (int(WIDTH * 0.75), int(HEIGHT * 0.16))
            beam_count = 14
            base_angle = t * 18.0  # continuous rotation
            for b_i in range(beam_count):
                ang = math.radians(base_angle + (360 / beam_count) * b_i)
                ang2 = ang + math.radians(6)
                beam_len = 380 + 40 * math.sin(t * 2.5 + b_i)
                pt1 = sun_center
                pt2 = (sun_center[0] + beam_len * math.cos(ang), sun_center[1] + beam_len * math.sin(ang))
                pt3 = (sun_center[0] + beam_len * math.cos(ang2), sun_center[1] + beam_len * math.sin(ang2))
                b_alpha = int(45 * sun_intensity * (0.6 + 0.4 * math.sin(t * 3.0 + b_i)))
                draw_ov.polygon([pt1, pt2, pt3], fill=(255, 240, 150, b_alpha))

        # Effect 3: Rainbow Burst & Floating Magical Sparkles (Active from 25s onward)
        if t >= 25.0:
            rb_intensity = min(1.0, (t - 25.0) / 4.0)
            # Radiant rainbow shimmer glow wave
            for spark in sparkles:
                spark["x"] = (spark["x"] + spark["vx"] * (1 / FPS)) % (WIDTH - 100)
                spark["y"] = (spark["y"] + spark["vy"] * (1 / FPS))
                if spark["y"] > 850 or spark["y"] < 250:
                    spark["y"] = random.uniform(280, 720)
                s_alpha = int(190 * rb_intensity * (0.5 + 0.5 * math.sin(t * 4.0 + spark["phase"])))
                sr = spark["radius"] + 2 * math.sin(t * 5.0 + spark["phase"])
                sc = spark["color"]
                draw_ov.ellipse([spark["x"] - sr * 2, spark["y"] - sr * 2, spark["x"] + sr * 2, spark["y"] + sr * 2], fill=(sc[0], sc[1], sc[2], int(s_alpha * 0.35)))
                draw_ov.ellipse([spark["x"] - sr, spark["y"] - sr, spark["x"] + sr, spark["y"] + sr], fill=(sc[0], sc[1], sc[2], s_alpha))

        # Kinetic Subtitles
        active_sub = None
        for s_start, s_end, txt in captions:
            if s_start <= t < s_end:
                active_sub = (s_start, s_end, txt)
                break

        if active_sub:
            s_start, s_end, text = active_sub
            dt = t - s_start
            scale = 1.0 if dt > 0.35 else min(1.0, 0.75 + 0.3 * math.sin(dt / 0.35 * math.pi * 1.5))
            box_w = int(960 * scale)
            box_h = 160
            box_x = (WIDTH - box_w) // 2
            box_y = HEIGHT - 270

            draw_ov.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=28, fill=(15, 30, 48, 215), outline=(100, 200, 255, 235), width=4)
            lines = wrap_text(text, font_sub, box_w - 60, draw_ov)
            total_text_h = len(lines) * 48
            start_ty = box_y + (box_h - total_text_h) // 2
            for i, line in enumerate(lines):
                line_bbox = draw_ov.textbbox((0, 0), line, font=font_sub)
                lw = line_bbox[2] - line_bbox[0]
                tx = box_x + (box_w - lw) // 2
                ty = start_ty + i * 48
                draw_ov.text((tx + 2, ty + 2), line, font=font_sub, fill=(0, 0, 0, 230))
                draw_ov.text((tx, ty), line, font=font_sub, fill=(255, 255, 245, 255))

        final_frame = Image.alpha_composite(frame, overlay)
        proc.stdin.write(final_frame.tobytes())

        if f_idx % (FPS * 5) == 0:
            print(f"  Pip: {f_idx}/{total_frames} frames rendered ({t:.1f}s)...")

    proc.stdin.close()
    proc.wait()
    print(f"Short #2 successfully rendered: {output_path}")

# -------------------------------------------------------------
# ANIMATION SUBSYSTEM: OLIVER THE OWL AND THE STARS
# -------------------------------------------------------------
def render_oliver_short(output_path, audio_path, duration=43.78):
    print(f"--- Rendering Animated Short #3: Oliver the Owl ({duration}s @ {FPS}fps) ---")
    base_img = Image.open(os.path.join(ASSETS_DIR, "oliver.jpg")).convert("RGBA")
    UP_W, UP_H = 1512, 2688
    base_large = base_img.resize((UP_W, UP_H), Image.Resampling.LANCZOS)

    captions = [
        (0.0, 7.0, "Oliver was a baby owl in a cozy hollow tree. But Oliver was afraid of the dark!"),
        (7.0, 13.5, "When the sun went down, Oliver hid under his soft wings."),
        (13.5, 20.5, "Then, a tiny sparkling firefly named Lumina tapped gently on his beak!"),
        (20.5, 28.0, "'Oliver, peek outside! The dark is just the blanket that lets the sparkly stars play!'"),
        (28.0, 36.0, "Oliver opened his big golden eyes. The forest glowed with moonlight and shooting stars! ⭐"),
        (36.0, duration, "It wasn't scary at all; it was wondrous. Close your eyes, little explorer. ✨🦉")
    ]

    total_frames = int(duration * FPS)

    # 70 Pulsing Twinkling Stars
    random.seed(777)
    stars = [
        {
            "x": random.uniform(80, WIDTH - 80),
            "y": random.uniform(50, int(HEIGHT * 0.45)),
            "base_r": random.uniform(2.5, 5.5),
            "freq": random.uniform(1.8, 4.5),
            "phase": random.uniform(0, math.pi * 2),
            "points": random.choice([4, 5, 0])  # 0 = glowing dot, 4 = 4-point cross
        }
        for _ in range(70)
    ]

    # 4 Shooting Stars trigger at t=4.5s, 15.0s, 25.5s, 35.0s
    shooting_stars_schedule = [
        {"start_t": 4.5, "duration": 1.2, "x1": 850, "y1": 80, "x2": 320, "y2": 420},
        {"start_t": 15.0, "duration": 1.1, "x1": 980, "y1": 150, "x2": 450, "y2": 520},
        {"start_t": 25.5, "duration": 1.3, "x1": 750, "y1": 60, "x2": 210, "y2": 460},
        {"start_t": 35.0, "duration": 1.2, "x1": 920, "y1": 110, "x2": 380, "y2": 490},
    ]

    # Firefly Lumina Stardust Trail
    firefly_trail = []

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgba",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-r", str(FPS),
        "-i", "-",
        "-i", audio_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_path
    ]
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    font_sub = get_font(38)

    for f_idx in range(total_frames):
        t = f_idx / FPS

        # Camera choreography:
        # 0-14s: close on baby Oliver shivering
        # 14-28s: slow pan towards Lumina the firefly
        # 28-44s: slow majestic upward panoramic drift into the starry moonlit night
        if t < 14.0:
            pan_x_pct = 0.44 + 0.02 * math.sin(t * 0.4)
            pan_y_pct = 0.54 + 0.02 * math.sin(t * 0.35)
            zoom = 1.18 + 0.03 * math.sin(t * 0.9)
        elif t < 28.0:
            p = (t - 14.0) / 14.0
            pan_x_pct = 0.44 + 0.08 * p
            pan_y_pct = 0.54 - 0.06 * p
            zoom = 1.18 - 0.06 * p
        else:
            p = (t - 28.0) / (duration - 28.0)
            pan_x_pct = 0.50 + 0.02 * math.sin(t * 0.3)
            pan_y_pct = 0.48 - 0.12 * p
            zoom = 1.12 + 0.04 * math.sin(t * 0.5)

        crop_w = int(WIDTH / zoom)
        crop_h = int(HEIGHT / zoom)
        x0 = max(0, min(UP_W - crop_w, int(UP_W * pan_x_pct - crop_w / 2)))
        y0 = max(0, min(UP_H - crop_h, int(UP_H * pan_y_pct - crop_h / 2)))

        frame_crop = base_large.crop((x0, y0, x0 + crop_w, y0 + crop_h))
        frame = frame_crop.resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)

        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)

        # 1. Twinkling Stars Animation
        for star in stars:
            pulse = 0.35 + 0.65 * math.sin(t * star["freq"] + star["phase"])
            if pulse > 0:
                s_alpha = int(220 * pulse)
                r = star["base_r"] * (0.8 + 0.5 * pulse)
                sx, sy = star["x"], star["y"]
                # Glow halo
                draw_ov.ellipse([sx - r * 2.5, sy - r * 2.5, sx + r * 2.5, sy + r * 2.5], fill=(220, 235, 255, int(s_alpha * 0.3)))
                if star["points"] == 4:
                    # 4-point sparkle cross
                    draw_ov.line([(sx - r * 3, sy), (sx + r * 3, sy)], fill=(255, 255, 255, s_alpha), width=2)
                    draw_ov.line([(sx, sy - r * 3), (sx, sy + r * 3)], fill=(255, 255, 255, s_alpha), width=2)
                draw_ov.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255, s_alpha))

        # 2. Shooting Stars Animation
        for ss in shooting_stars_schedule:
            if ss["start_t"] <= t <= (ss["start_t"] + ss["duration"]):
                progress = (t - ss["start_t"]) / ss["duration"]
                head_x = ss["x1"] + (ss["x2"] - ss["x1"]) * progress
                head_y = ss["y1"] + (ss["y2"] - ss["y1"]) * progress
                tail_len = 140
                tail_x = head_x - tail_len * (ss["x2"] - ss["x1"]) / 600
                tail_y = head_y - tail_len * (ss["y2"] - ss["y1"]) / 600

                ss_alpha = int(255 * math.sin(progress * math.pi))
                # Draw radiant shooting star beam
                draw_ov.line([(tail_x, tail_y), (head_x, head_y)], fill=(220, 240, 255, ss_alpha), width=4)
                draw_ov.ellipse([head_x - 7, head_y - 7, head_x + 7, head_y + 7], fill=(255, 255, 255, ss_alpha))
                draw_ov.ellipse([head_x - 14, head_y - 14, head_x + 14, head_y + 14], fill=(180, 220, 255, int(ss_alpha * 0.4)))

        # 3. Dynamic Flying Lumina the Firefly with Stardust Trail
        # Orbit around Oliver in a graceful 3D Lissajous curve
        center_fx = WIDTH * 0.68
        center_fy = HEIGHT * 0.46
        fx = center_fx + 120 * math.cos(t * 1.6) + 40 * math.sin(t * 3.2)
        fy = center_fy + 85 * math.sin(t * 1.8) + 30 * math.cos(t * 2.5)

        # Record stardust trail
        if f_idx % 2 == 0:
            firefly_trail.append({"x": fx, "y": fy, "birth_t": t, "r": random.uniform(2, 5)})
        # Keep trail fresh (last 1.5 seconds)
        firefly_trail = [p for p in firefly_trail if (t - p["birth_t"]) < 1.4]

        # Draw Stardust Trail
        for p in firefly_trail:
            age = t - p["birth_t"]
            fade = max(0.0, 1.0 - age / 1.4)
            p_alpha = int(210 * fade)
            pr = p["r"] * fade
            draw_ov.ellipse([p["x"] - pr, p["y"] - pr, p["x"] + pr, p["y"] + pr], fill=(255, 235, 120, p_alpha))

        # Draw Lumina's Glowing Body & Pulsing Halo
        lumina_pulse = 0.7 + 0.3 * math.sin(t * 5.0)
        halo_r = 38 * lumina_pulse
        draw_ov.ellipse([fx - halo_r * 2.2, fy - halo_r * 2.2, fx + halo_r * 2.2, fy + halo_r * 2.2], fill=(255, 215, 60, int(70 * lumina_pulse)))
        draw_ov.ellipse([fx - halo_r, fy - halo_r, fx + halo_r, fy + halo_r], fill=(255, 235, 100, int(150 * lumina_pulse)))
        draw_ov.ellipse([fx - 9, fy - 9, fx + 9, fy + 9], fill=(255, 255, 220, 255))

        # Kinetic Subtitles
        active_sub = None
        for s_start, s_end, txt in captions:
            if s_start <= t < s_end:
                active_sub = (s_start, s_end, txt)
                break

        if active_sub:
            s_start, s_end, text = active_sub
            dt = t - s_start
            scale = 1.0 if dt > 0.35 else min(1.0, 0.75 + 0.3 * math.sin(dt / 0.35 * math.pi * 1.5))
            box_w = int(960 * scale)
            box_h = 160
            box_x = (WIDTH - box_w) // 2
            box_y = HEIGHT - 270

            draw_ov.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=28, fill=(10, 15, 35, 220), outline=(255, 215, 80, 240), width=4)
            lines = wrap_text(text, font_sub, box_w - 60, draw_ov)
            total_text_h = len(lines) * 48
            start_ty = box_y + (box_h - total_text_h) // 2
            for i, line in enumerate(lines):
                line_bbox = draw_ov.textbbox((0, 0), line, font=font_sub)
                lw = line_bbox[2] - line_bbox[0]
                tx = box_x + (box_w - lw) // 2
                ty = start_ty + i * 48
                draw_ov.text((tx + 2, ty + 2), line, font=font_sub, fill=(0, 0, 0, 230))
                draw_ov.text((tx, ty), line, font=font_sub, fill=(255, 255, 245, 255))

        final_frame = Image.alpha_composite(frame, overlay)
        proc.stdin.write(final_frame.tobytes())

        if f_idx % (FPS * 5) == 0:
            print(f"  Oliver: {f_idx}/{total_frames} frames rendered ({t:.1f}s)...")

    proc.stdin.close()
    proc.wait()
    print(f"Short #3 successfully rendered: {output_path}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    render_barnaby_short(
        os.path.join(OUTPUT_DIR, "shorts_1.mp4"),
        os.path.join(OUTPUT_DIR, "short1_audio.mp3"),
        duration=40.18
    )
    render_pip_short(
        os.path.join(OUTPUT_DIR, "shorts_2.mp4"),
        os.path.join(OUTPUT_DIR, "short2_audio.mp3"),
        duration=40.46
    )
    render_oliver_short(
        os.path.join(OUTPUT_DIR, "shorts_3.mp4"),
        os.path.join(OUTPUT_DIR, "short3_audio.mp3"),
        duration=43.78
    )
    print("\n🎉 ALL 3 FULLY ANIMATED KIDS SHORTS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
