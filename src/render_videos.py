#!/usr/bin/env python3
"""
Complete Video Assembly Engine for Autonomous YouTube Studio
Renders:
- final_video.mp4 (16:9, 1080p, 7m 05s, changing visuals every 7-8s)
- preview_first_60s.mp4 (First 60s of long video)
- shorts_1.mp4 (9:16 vertical, 55.75s)
- shorts_2.mp4 (9:16 vertical, 56.40s)
- shorts_3.mp4 (9:16 vertical, 58.10s, with prominent on-screen 'NOT FINANCIAL ADVICE')
"""

import os
import subprocess

OUTPUT_DIR = "output/saaspocalypse-ai-agents"
FRAMES_DIR = "output/saaspocalypse-ai-agents/render_frames"
CHARTS_DIR = "output/saaspocalypse-ai-agents/charts"

def generate_subtitles():
    # Long video subtitles (424.5s)
    srt_long = """1
00:00:00,000 --> 00:00:04,500
For twenty years, enterprise software ran on a simple business model:

2
00:00:04,500 --> 00:00:09,500
build a web dashboard, charge a monthly fee for every employee who logs in,

3
00:00:09,500 --> 00:00:13,800
and scale recurring revenue directly by seat count.

4
00:00:14,000 --> 00:00:18,500
But according to a major forecast from research firm Gartner,

5
00:00:18,500 --> 00:00:23,800
up to $234 billion in enterprise application software spending is now at risk by 2030.

6
00:00:24,000 --> 00:00:27,500
Not because companies are using less software...

7
00:00:27,500 --> 00:00:32,800
but because autonomous AI agents are beginning to bypass human dashboards.

8
00:00:33,000 --> 00:00:38,500
To understand why this shift is happening, look at how software evolved over two decades.

9
00:00:38,500 --> 00:00:44,000
Back in the early 2000s, software moved from CD-ROMs to recurring cloud subscriptions.

10
00:00:44,000 --> 00:00:50,000
Vendors realized they could charge per employee, every single month, forever.

11
00:00:50,000 --> 00:00:56,000
This created the per-seat model: 10,000 employees meant 10,000 software licenses.

12
00:00:56,000 --> 00:01:03,000
For twenty years, Wall Street celebrated this as the most predictable model in tech.

13
00:01:03,000 --> 00:01:10,000
Software was evaluated on interface design, menus, and screens built for human clicks.

14
00:01:10,000 --> 00:01:17,000
As Gartner VP George Brocklehurst noted: all that usability and workflow training depreciates.

15
00:01:17,000 --> 00:01:25,000
In research published by Gartner, analysts estimate up to $234B in SaaS spending exposed to agentic arbitrage.

16
00:01:25,000 --> 00:01:32,000
That accounts for approximately twenty percent of overall enterprise SaaS spending by 2030.

17
00:01:32,000 --> 00:01:39,000
Agentic arbitrage means AI agents complete tasks across systems, reducing need for human interfaces.

18
00:01:39,000 --> 00:01:46,000
An agent does not need a visual UI. It communicates directly through APIs and databases.

19
00:01:46,000 --> 00:01:54,000
When agents reconcile data and execute cross-platform tasks, the software interface becomes invisible.

20
00:01:54,000 --> 00:02:02,000
This breaks the link between employee headcount and software licensing revenue.

21
00:02:02,000 --> 00:02:11,000
In August 2024, Klarna CEO Sebastian Siemiatkowski stated publicly on an investor call:

22
00:02:11,000 --> 00:02:19,000
"As an example, we just shut down Salesforce. Within a few weeks, we will shut down Workday."

23
00:02:19,000 --> 00:02:27,000
"We are shutting down a lot of our SaaS providers, as we are able to consolidate."

24
00:02:27,000 --> 00:02:35,000
Industry reporting confirmed that human escalation remained critical for complex customer disputes.

25
00:02:35,000 --> 00:02:44,000
What Klarna proved was an aggressive enterprise push to consolidate vendors and eliminate redundant seats.

26
00:02:44,000 --> 00:02:53,000
However, Gartner warns: more than 40% of agentic AI projects will be canceled by end of 2027.

27
00:02:53,000 --> 00:03:01,000
Why? Complex reasoning loops consume massive tokens, and unmonitored agents create enterprise liability.

28
00:03:01,000 --> 00:03:09,000
As Gartner analyst George Brocklehurst emphasized: SaaS will not be destroyed; it will emerge in a different form.

29
00:03:09,000 --> 00:03:17,000
This is less an apocalypse and more of a metamorphosis.

30
00:03:17,000 --> 00:03:26,000
Thin interface dashboards face high exposure, while deep systems of record remain resilient.

31
00:03:26,000 --> 00:03:35,000
Vendors are transitioning from per-seat fees to outcome-based and consumption-based models.

32
00:03:35,000 --> 00:03:44,000
Value shifts from the visual dashboard to underlying data and API orchestration layers.

33
00:03:44,000 --> 00:04:24,000
Note: this analysis is for educational purposes only and does not constitute financial or legal advice.
"""
    with open(os.path.join(OUTPUT_DIR, "full_captions.srt"), "w") as f:
        f.write(srt_long.strip())

    # Short 1 SRT
    srt_s1 = """1
00:00:00,000 --> 00:00:07,000
For twenty years, corporations paid a monthly fee for every employee who logged into software.

2
00:00:07,000 --> 00:00:15,000
Research firm Gartner estimates up to $234 billion in SaaS spending is at risk from agentic arbitrage by 2030.

3
00:00:15,000 --> 00:00:24,000
Autonomous AI agents don't interact through dashboards; they execute workflows directly via APIs.

4
00:00:24,000 --> 00:00:34,000
When agents automate tasks across systems, the historic link between headcount and software licensing breaks down.

5
00:00:34,000 --> 00:00:44,000
As Gartner notes, SaaS is not disappearing, but the way we buy and price software is fundamentally transforming.

6
00:00:44,000 --> 00:00:55,000
Watch our full breakdown on our channel for the complete data.
"""
    with open(os.path.join(OUTPUT_DIR, "short1_captions.srt"), "w") as f:
        f.write(srt_s1.strip())

    # Short 2 SRT
    srt_s2 = """1
00:00:00,000 --> 00:00:07,000
What did Klarna's CEO actually say when headlines reported they were dropping major software vendors?

2
00:00:07,000 --> 00:00:15,000
During an August 2024 earnings call, Klarna CEO Sebastian Siemiatkowski stated:

3
00:00:15,000 --> 00:00:25,000
"As an example, we just shut down Salesforce. Within a few weeks, we will shut down Workday."

4
00:00:25,000 --> 00:00:35,000
"We are shutting down a lot of our SaaS providers, as we are able to consolidate."

5
00:00:35,000 --> 00:00:45,000
While headlines suggested software vanished overnight, human support escalation remains essential for complex disputes.

6
00:00:45,000 --> 00:00:56,000
Enterprise buyers are actively consolidating vendors to eliminate redundant software seats.
"""
    with open(os.path.join(OUTPUT_DIR, "short2_captions.srt"), "w") as f:
        f.write(srt_s2.strip())

    # Short 3 SRT
    srt_s3 = """1
00:00:00,000 --> 00:00:08,000
Note: this analysis is for educational purposes only and does not constitute financial advice.

2
00:00:08,000 --> 00:00:16,000
With Gartner estimating up to $234 billion in SaaS spending at risk by 2030, which categories are most exposed?

3
00:00:16,000 --> 00:00:27,000
High Exposure: Thin interface tools providing forms or basic workflow routing screens bypassed by APIs.

4
00:00:27,000 --> 00:00:38,000
High Resilience: Systems of record housing authoritative transaction ledgers and secure backends.

5
00:00:38,000 --> 00:00:48,000
As Gartner analyst George Brocklehurst noted: SaaS will not be destroyed; it will emerge in a different form.

6
00:00:48,000 --> 00:00:58,000
Watch the full video on our channel for the complete breakdown.
"""
    with open(os.path.join(OUTPUT_DIR, "short3_captions.srt"), "w") as f:
        f.write(srt_s3.strip())

    print("Subtitles generated.")

def render_long_video():
    print("Rendering final_video.mp4 (16:9 Long Video, 7m 05s)...")
    
    # We create a sequence of 54 slides by alternating between long_01..long_22 and the 4 compliant charts
    # Every slide displays for 7.86 seconds -> 54 * 7.86 = 424.5s
    slide_files = []
    base_slides = [f"long_{i:02d}.png" for i in range(1, 23)]
    charts = ["scene1_evolution.png", "scene2_gartner_share.png", "scene3_workflow_comparison.png", "scene4_resilience_matrix.png"]
    
    for i in range(27):
        slide_files.append(os.path.join(FRAMES_DIR, base_slides[i % len(base_slides)]))
        slide_files.append(os.path.join(CHARTS_DIR, charts[i % len(charts)]))
    
    # Write FFmpeg concat file
    concat_txt = os.path.join(OUTPUT_DIR, "long_concat.txt")
    with open(concat_txt, "w") as f:
        for sf in slide_files[:54]:
            f.write(f"file '{os.path.abspath(sf)}'\n")
            f.write("duration 7.86\n")
        f.write(f"file '{os.path.abspath(slide_files[-1])}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-i", os.path.join(OUTPUT_DIR, "full_voiceover.mp3"),
        "-vf", f"scale=1920:1080,subtitles={os.path.join(OUTPUT_DIR, 'full_captions.srt')}:force_style='FontName=Liberation Sans,FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,MarginV=40'",
        "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        os.path.join(OUTPUT_DIR, "final_video.mp4")
    ]
    subprocess.check_call(cmd)
    print("final_video.mp4 rendered successfully!")

    # Render first 60 seconds preview
    print("Rendering preview_first_60s.mp4...")
    cmd_preview = [
        "ffmpeg", "-y",
        "-ss", "0", "-t", "60",
        "-i", os.path.join(OUTPUT_DIR, "final_video.mp4"),
        "-c", "copy",
        os.path.join(OUTPUT_DIR, "preview_first_60s.mp4")
    ]
    subprocess.check_call(cmd_preview)
    print("preview_first_60s.mp4 rendered successfully!")

def render_shorts():
    print("Rendering 3 Shorts (9:16 Vertical)...")
    
    shorts_cfg = [
        ("shorts_1.mp4", "short1_voiceover.mp3", "short1_captions.srt", "short1_01.png", 55.75),
        ("shorts_2.mp4", "short2_voiceover.mp3", "short2_captions.srt", "short2_01.png", 56.40),
        ("shorts_3.mp4", "short3_voiceover.mp3", "short3_captions.srt", "short3_01.png", 58.10),
    ]
    
    for out_name, audio_name, srt_name, frame_name, duration in shorts_cfg:
        print(f"Rendering {out_name}...")
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-t", str(duration), "-i", os.path.join(FRAMES_DIR, frame_name),
            "-i", os.path.join(OUTPUT_DIR, audio_name),
            "-vf", f"scale=1080:1920,subtitles={os.path.join(OUTPUT_DIR, srt_name)}:force_style='FontName=Liberation Sans,FontSize=28,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,MarginV=120'",
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            os.path.join(OUTPUT_DIR, out_name)
        ]
        subprocess.check_call(cmd)
        print(f"{out_name} rendered successfully!")

if __name__ == "__main__":
    generate_subtitles()
    render_long_video()
    render_shorts()
    print("ALL MEDIA PRODUCTION COMPLETED.")
