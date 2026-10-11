#!/usr/bin/env python3
"""
Kids Shorts Video Rendering Engine
Renders 3 beautiful, vertical 1080x1920 YouTube Shorts for Kids Bedtime Fables:
- shorts_1.mp4: Barnaby the Bear Who Lost His Roar (40.18s)
- shorts_2.mp4: Pip the Little Cloud Who Wanted a Rainbow (40.46s)
- shorts_3.mp4: Oliver the Owl Who Loved the Stars (43.78s)
Audio: Warm Jenny voice mixed with custom soothing music box lullaby
"""

import os
import subprocess

OUTPUT_DIR = "output/kids-bedtime-fables"
FRAMES_DIR = "output/kids-bedtime-fables/render_frames"

def generate_kids_subtitles():
    srt1 = """1
00:00:00,000 --> 00:00:06,500
One sunny morning in Whispering Woods, Barnaby the Bear woke up, and his roar was gone!

2
00:00:06,500 --> 00:00:13,000
Instead of a big roar, all that came out was a tiny, gentle squeak.

3
00:00:13,000 --> 00:00:19,500
Barnaby felt terribly embarrassed. How could he be brave without a loud voice?

4
00:00:19,500 --> 00:00:26,000
On his quiet walk, he found a tiny lost bunny shivering in the tall grass.

5
00:00:26,000 --> 00:00:33,500
Barnaby spoke so softly that the bunny stopped crying, giggled, and hopped up.

6
00:00:33,500 --> 00:00:40,180
Barnaby smiled. Being kind and gentle is the bravest thing of all. Sweet dreams!
"""
    with open(os.path.join(OUTPUT_DIR, "short1_captions.srt"), "w") as f:
        f.write(srt1.strip())

    srt2 = """1
00:00:00,000 --> 00:00:06,500
High in the sky, Pip the little cloud wanted to make a rainbow all by himself.

2
00:00:06,500 --> 00:00:13,500
Pip puffed his cheeks and rained and rained. But all he made was a gray puddle.

3
00:00:13,500 --> 00:00:20,000
He felt sad and began to sigh. Then, Sunny the golden sun peeked out with a warm smile.

4
00:00:20,000 --> 00:00:26,500
"You have raindrops, Pip, and I have golden light. Let us make one together!"

5
00:00:26,500 --> 00:00:33,500
Sunny shone through Pip's raindrops, and a bright rainbow painted the entire sky!

6
00:00:33,500 --> 00:00:40,460
Pip laughed with joy. Together, they made magic. Sleep tight, sweet dreamer!
"""
    with open(os.path.join(OUTPUT_DIR, "short2_captions.srt"), "w") as f:
        f.write(srt2.strip())

    srt3 = """1
00:00:00,000 --> 00:00:07,000
Oliver was a baby owl in a cozy hollow tree. But Oliver had a secret: he was afraid of the dark!

2
00:00:07,000 --> 00:00:13,500
When the sun went down, Oliver hid under his soft wings.

3
00:00:13,500 --> 00:00:20,500
Then, a tiny sparkling firefly named Lumina tapped gently on his beak.

4
00:00:20,500 --> 00:00:28,000
"Oliver, peek outside! The dark is just the blanket that lets the sparkly stars play!"

5
00:00:28,000 --> 00:00:36,000
Oliver opened his big golden eyes. The forest glowed with moonlight and shooting stars.

6
00:00:36,000 --> 00:00:43,780
It was not scary at all; it was wondrous. Close your eyes, little explorer.
"""
    with open(os.path.join(OUTPUT_DIR, "short3_captions.srt"), "w") as f:
        f.write(srt3.strip())

    print("Kids subtitles updated.")

def render_all_kids_shorts():
    shorts = [
        ("shorts_1.mp4", "short1_audio.mp3", "short1_captions.srt", ["short1_01.png", "short1_02.png", "short1_03.png"], 40.18),
        ("shorts_2.mp4", "short2_audio.mp3", "short2_captions.srt", ["short2_01.png", "short2_02.png", "short2_03.png"], 40.46),
        ("shorts_3.mp4", "short3_audio.mp3", "short3_captions.srt", ["short3_01.png", "short3_02.png", "short3_03.png"], 43.78),
    ]

    for out_name, audio_name, srt_name, frame_list, duration in shorts:
        print(f"Rendering {out_name} (duration: {duration}s)...")
        per_slide = duration / len(frame_list)

        # Concat script for frames
        concat_txt = os.path.join(OUTPUT_DIR, f"{out_name}_concat.txt")
        with open(concat_txt, "w") as f:
            for fr in frame_list:
                f.write(f"file '{os.path.abspath(os.path.join(FRAMES_DIR, fr))}'\n")
                f.write(f"duration {per_slide:.2f}\n")
            f.write(f"file '{os.path.abspath(os.path.join(FRAMES_DIR, frame_list[-1]))}'\n")

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", concat_txt,
            "-i", os.path.join(OUTPUT_DIR, audio_name),
            "-vf", f"scale=1080:1920,subtitles={os.path.join(OUTPUT_DIR, srt_name)}:force_style='FontName=Liberation Sans,FontSize=30,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,MarginV=100'",
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            os.path.join(OUTPUT_DIR, out_name)
        ]
        subprocess.check_call(cmd)
        print(f"{out_name} rendered successfully!")

if __name__ == "__main__":
    generate_kids_subtitles()
    render_all_kids_shorts()
    print("ALL KIDS SHORTS RENDERED WITH SOOTHING LULLABY AUDIO.")
