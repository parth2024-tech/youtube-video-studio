#!/usr/bin/env python3
"""
Audio Synthesizer for Kids Bedtime Fables
Voice: en-US-JennyNeural (Warm, maternal, gentle storyteller)
Features:
- Natural pacing with clean punctuation (no robotic ellipsis glitches)
- Custom-synthesized soothing music box lullaby backing track
- Studio audio mixing with warm EQ
"""

import os
import asyncio
import numpy as np
from scipy.io import wavfile
import subprocess
import edge_tts

OUTPUT_DIR = "output/kids-bedtime-fables"
VOICE = "en-US-JennyNeural"

# Clean, natural storytelling scripts with human punctuation
STORY_1 = (
    "One sunny morning in Whispering Woods, Barnaby the Bear woke up, and his mighty roar was gone. "
    "Instead of a big roar, all that came out was a tiny, gentle squeak. "
    "Barnaby felt terribly embarrassed. How could he be a brave bear without a loud voice? "
    "But on his quiet walk, he found a tiny lost bunny shivering in the tall grass. "
    "When Barnaby spoke, his voice was so soft and gentle that the bunny stopped crying, giggled, and hopped onto his shoulder. "
    "Barnaby smiled. He learned that being kind and gentle is the bravest thing of all. "
    "Sweet dreams, little one."
)

STORY_2 = (
    "High in the sky, Pip the little cloud had a big dream: he wanted to make a rainbow all by himself. "
    "Pip puffed his cheeks and rained and rained. But all he made was a gray, gloomy puddle. "
    "He felt sad and began to sigh. "
    "Then, Sunny the golden sun peeked out and said, 'Pip, you have the raindrops, but I have the warm golden light. Let us make one together!' "
    "Sunny shone through Pip's raindrops, and suddenly, a bright, beautiful rainbow painted the entire sky! "
    "Pip laughed with joy. Together, they made magic. "
    "Sleep tight, sweet dreamer."
)

STORY_3 = (
    "Oliver was a little baby owl who lived in a cozy hollow tree. But Oliver had a secret: he was afraid of the dark. "
    "When the sun went down, Oliver hid under his soft wings. "
    "Then, a tiny sparkling firefly named Lumina tapped gently on his beak. "
    "'Oliver, peek outside,' Lumina whispered. 'The dark is just the cozy blanket that lets the sparkly stars play!' "
    "Oliver opened his big golden eyes. The nighttime forest was glowing with moonlight, fireflies, and shooting stars. "
    "It was not scary at all; it was wondrous. "
    "Close your eyes, little explorer. The night is watching over you."
)

def generate_lullaby_music_track(output_wav_path, duration=50.0):
    """Synthesizes a gentle, calming music box / celesta lullaby bed."""
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # Note frequencies
    C4, D4, E4, F4, G4, A4, B4 = 261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88
    C5, D5, E5, G5 = 523.25, 587.33, 659.25, 783.99

    melody_pattern = [
        # Bar 1: Cmaj7 arpeggio
        (0.0, C4, 1.8), (0.5, G4, 1.5), (1.0, E5, 2.0), (1.5, B4, 1.8),
        (2.0, G4, 1.5), (2.5, E5, 2.0), (3.0, C5, 2.2), (3.5, G4, 1.5),
        # Bar 2: Am9 arpeggio
        (4.0, 220.0, 1.8), (4.5, E4, 1.5), (5.0, C5, 2.0), (5.5, G4, 1.8),
        (6.0, E4, 1.5), (6.5, C5, 2.0), (7.0, A4, 2.2), (7.5, E4, 1.5),
        # Bar 3: Fmaj7 arpeggio
        (8.0, 174.61, 1.8), (8.5, C4, 1.5), (9.0, A4, 2.0), (9.5, E5, 1.8),
        (10.0, C4, 1.5), (10.5, A4, 2.0), (11.0, F4, 2.2), (11.5, C4, 1.5),
        # Bar 4: G7 arpeggio
        (12.0, 196.0, 1.8), (12.5, D4, 1.5), (13.0, B4, 2.0), (13.5, D5, 1.8),
        (14.0, G4, 1.5), (14.5, B4, 2.0), (15.0, G4, 2.2), (15.5, D4, 1.5),
    ]

    all_notes = []
    loops = int(duration // 16.0) + 2
    for loop in range(loops):
        offset = loop * 16.0
        for start, freq, note_len in melody_pattern:
            if start + offset < duration:
                all_notes.append((start + offset, freq, note_len))

    left = np.zeros(len(t))
    right = np.zeros(len(t))

    for start_time, freq, note_len in all_notes:
        idx_start = int(start_time * sample_rate)
        note_samples = int(note_len * sample_rate)
        idx_end = min(idx_start + note_samples, len(t))
        actual_len = idx_end - idx_start
        if actual_len <= 0:
            continue
        time_chunk = np.linspace(0, note_len, note_samples)[:actual_len]

        # Celesta / Music Box envelope
        env = np.exp(-time_chunk * 2.2) * (1.0 - np.exp(-time_chunk * 80.0))
        wave = (
            0.70 * np.sin(2 * np.pi * freq * time_chunk) +
            0.20 * np.sin(2 * np.pi * 2 * freq * time_chunk) +
            0.07 * np.sin(2 * np.pi * 3 * freq * time_chunk) +
            0.03 * np.sin(2 * np.pi * 4 * freq * time_chunk)
        ) * env

        pan = 0.5 + 0.3 * np.sin(freq * 0.05)
        left[idx_start:idx_end] += wave * (1.0 - pan)
        right[idx_start:idx_end] += wave * pan

    # Gentle ambient delay / reverb
    delay_samples = int(0.35 * sample_rate)
    for i in range(delay_samples, len(left)):
        left[i] += left[i - delay_samples] * 0.30
        right[i] += right[i - delay_samples] * 0.30

    # Normalization & soft 16-bit master
    max_val = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-6)
    left = (left / max_val * 0.55 * 32767).astype(np.int16)
    right = (right / max_val * 0.55 * 32767).astype(np.int16)

    stereo = np.column_stack((left, right))
    wavfile.write(output_wav_path, sample_rate, stereo)
    print(f"Generated lullaby music bed at: {output_wav_path}")

async def synthesize_voice_and_mix():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    lullaby_wav = os.path.join(OUTPUT_DIR, "lullaby_music_box.wav")
    generate_lullaby_music_track(lullaby_wav, duration=55.0)

    stories = [
        ("short1", STORY_1),
        ("short2", STORY_2),
        ("short3", STORY_3),
    ]

    for prefix, text in stories:
        raw_voice_mp3 = os.path.join(OUTPUT_DIR, f"{prefix}_raw_voice.mp3")
        final_mixed_mp3 = os.path.join(OUTPUT_DIR, f"{prefix}_audio.mp3")

        print(f"Synthesizing Jenny voice for {prefix}...")
        comm = edge_tts.Communicate(text, VOICE, rate="-5%", pitch="+0Hz")
        await comm.save(raw_voice_mp3)

        # Mix voiceover with soothing music bed and gentle EQ
        print(f"Mixing {prefix} with lullaby bed...")
        mix_cmd = [
            "ffmpeg", "-y",
            "-i", raw_voice_mp3,
            "-i", lullaby_wav,
            "-filter_complex",
            "[0:a]volume=1.1,equalizer=f=3500:width_type=o:w=1.0:g=-2.0[v];[1:a]volume=0.15[m];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]",
            "-map", "[a]",
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            final_mixed_mp3
        ]
        subprocess.check_call(mix_cmd)
        print(f"Successfully generated soothing mix: {final_mixed_mp3}")

if __name__ == "__main__":
    asyncio.run(synthesize_voice_and_mix())
