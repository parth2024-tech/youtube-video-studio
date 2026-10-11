#!/usr/bin/env python3
"""
Audio Synthesizer for Kids Bedtime Fables
Voice: en-US-AvaNeural (Warm, expressive, caring storyteller)
"""

import os
import asyncio
import edge_tts

OUTPUT_DIR = "output/kids-bedtime-fables"
VOICE = "en-US-AvaNeural"

STORY_1 = (
    "One sunny morning in Whispering Woods, Barnaby the Bear woke up... and his mighty roar was gone! ... "
    "Instead of a big ROAR, all that came out was a tiny little squeak. ... "
    "Barnaby felt terribly embarrassed. How could he be a big, brave bear without a loud voice? ... "
    "But on his walk, he found a tiny lost bunny shivering in the tall grass. ... "
    "When Barnaby spoke, his voice was so soft and gentle that the bunny stopped crying, giggled, and hopped onto his shoulder. ... "
    "Barnaby smiled. He learned that being kind and gentle is the bravest thing of all. ... "
    "Sweet dreams, little one."
)

STORY_2 = (
    "High in the sky, Pip the little cloud had a big dream: he wanted to make a rainbow all by himself. ... "
    "Pip puffed his cheeks and rained and rained. But all he made was a gray, gloomy puddle. ... "
    "He felt sad and began to sigh. ... "
    "Then, Sunny the golden sun peeked out and said: 'Pip, you have the raindrops, but I have the warm golden light. Let us make one together!' ... "
    "Sunny shone through Pip's raindrops... and suddenly, a bright, beautiful rainbow painted the entire sky! ... "
    "Pip laughed with joy. Together, they made magic. ... "
    "Sleep tight, sweet dreamer."
)

STORY_3 = (
    "Oliver was a little baby owl who lived in a cozy hollow tree. But Oliver had a secret: he was afraid of the dark! ... "
    "When the sun went down, Oliver hid under his wings. ... "
    "Then, a tiny sparkling firefly named Lumina tapped on his beak. ... "
    "'Oliver, peek outside,' Lumina whispered. 'The dark is just the blanket that lets the sparkly stars play!' ... "
    "Oliver opened his big golden eyes. The nighttime forest was glowing with moonlight, fireflies, and shooting stars. ... "
    "It was not scary at all; it was wondrous. ... "
    "Close your eyes, little explorer. The night is watching over you."
)

async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    tasks = [
        ("short1_audio.mp3", STORY_1),
        ("short2_audio.mp3", STORY_2),
        ("short3_audio.mp3", STORY_3),
    ]
    for filename, text in tasks:
        path = os.path.join(OUTPUT_DIR, filename)
        print(f"Synthesizing {filename}...")
        comm = edge_tts.Communicate(text, VOICE, rate="-4%", pitch="+2Hz")
        await comm.save(path)
        print(f"Saved {path}")

if __name__ == "__main__":
    asyncio.run(main())
