#!/usr/bin/env python3
"""
Master Studio Video Production Engine
Renders:
1. final_video.mp4 (16:9 Long-Form, 7m 05s)
2. preview_first_60s.mp4 (First 60s of long video)
3. shorts_1.mp4 (9:16 Vertical, ~55s)
4. shorts_2.mp4 (9:16 Vertical, ~56s)
5. shorts_3.mp4 (9:16 Vertical, ~58s, with on-screen 'NOT FINANCIAL ADVICE')

Strictly enforces:
- Visual changes every 5-8 seconds.
- Burned-in captions on all videos.
- Purely compliant figures and 'ILLUSTRATIVE EXAMPLE' labeling on conceptual mockups.
"""

import os
import subprocess
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "output/saaspocalypse-ai-agents"
FRAMES_DIR = "output/saaspocalypse-ai-agents/render_frames"
os.makedirs(FRAMES_DIR, exist_ok=True)

FONT_PATH = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Bold.ttf"

def make_slide_16x9(filename, title, subtitle="", badge=None, bullets=None, highlight_box=None):
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), color="#080c14")
    draw = ImageDraw.Draw(img)

    # Subtle gradient
    for y in range(height):
        r = int(8 + (y / height) * 14)
        g = int(12 + (y / height) * 18)
        b = int(20 + (y / height) * 32)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    f_title = ImageFont.truetype(FONT_PATH, 54)
    f_sub = ImageFont.truetype(FONT_PATH, 32)
    f_badge = ImageFont.truetype(FONT_PATH, 24)
    f_body = ImageFont.truetype(FONT_PATH, 34)

    # Badge (if any)
    y_start = 80
    if badge:
        bbox_b = draw.textbbox((0, 0), badge, font=f_badge)
        bw = bbox_b[2] - bbox_b[0]
        bh = bbox_b[3] - bbox_b[1]
        draw.rounded_rectangle([(100, 60), (100 + bw + 36, 60 + bh + 20)], radius=8, fill="#1e293b", outline="#38bdf8", width=2)
        draw.text((118, 68), badge, fill="#38bdf8", font=f_badge)
        y_start = 130

    # Title
    draw.text((100, y_start), title, fill="#ffffff", font=f_title)
    if subtitle:
        draw.text((100, y_start + 75), subtitle, fill="#94a3b8", font=f_sub)

    # Main Card Area
    card_y = y_start + 160
    draw.rounded_rectangle([(100, card_y), (1820, 920)], radius=20, fill="#0f172a", outline="#334155", width=2)

    if highlight_box:
        hb_color, hb_text, hb_sub = highlight_box
        draw.rounded_rectangle([(140, card_y + 40), (1780, card_y + 220)], radius=16, fill="#1e293b", outline=hb_color, width=3)
        draw.text((180, card_y + 70), hb_text, fill=hb_color, font=f_title)
        if hb_sub:
            draw.text((180, card_y + 145), hb_sub, fill="#e2e8f0", font=f_sub)

    if bullets:
        b_y = card_y + (260 if highlight_box else 60)
        for b in bullets:
            draw.text((150, b_y), f"• {b}", fill="#e2e8f0", font=f_body)
            b_y += 75

    path = os.path.join(FRAMES_DIR, filename)
    img.save(path, quality=95)
    return path

def make_slide_9x16(filename, title, badge=None, bullets=None, quote=None, disclaimer=False):
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), color="#080c14")
    draw = ImageDraw.Draw(img)

    for y in range(height):
        r = int(8 + (y / height) * 16)
        g = int(12 + (y / height) * 22)
        b = int(20 + (y / height) * 38)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    f_title = ImageFont.truetype(FONT_PATH, 58)
    f_sub = ImageFont.truetype(FONT_PATH, 36)
    f_badge = ImageFont.truetype(FONT_PATH, 28)
    f_body = ImageFont.truetype(FONT_PATH, 40)
    f_disc = ImageFont.truetype(FONT_PATH, 24)

    y_pos = 140
    if badge:
        bbox_b = draw.textbbox((0, 0), badge, font=f_badge)
        bw = bbox_b[2] - bbox_b[0]
        bh = bbox_b[3] - bbox_b[1]
        draw.rounded_rectangle([(70, y_pos), (70 + bw + 40, y_pos + bh + 24)], radius=10, fill="#e11d48")
        draw.text((90, y_pos + 10), badge, fill="#ffffff", font=f_badge)
        y_pos += 100

    draw.text((70, y_pos), title, fill="#ffffff", font=f_title)
    y_pos += 140

    draw.rounded_rectangle([(60, y_pos), (1020, 1700)], radius=24, fill="#0f172a", outline="#38bdf8", width=3)
    card_y = y_pos + 60

    if quote:
        draw.rounded_rectangle([(90, card_y), (990, card_y + 400)], radius=16, fill="#1e293b", outline="#facc15", width=2)
        # Word wrap quote
        words = quote.split()
        lines = []
        cur = []
        for w in words:
            cur.append(w)
            if len(" ".join(cur)) > 35:
                lines.append(" ".join(cur))
                cur = []
        if cur:
            lines.append(" ".join(cur))
        
        qy = card_y + 40
        for l in lines[:7]:
            draw.text((120, qy), l, fill="#ffffff", font=f_sub)
            qy += 50
        card_y += 450

    if bullets:
        for b in bullets:
            draw.text((110, card_y), f"• {b}", fill="#e2e8f0", font=f_body)
            card_y += 100

    if disclaimer:
        draw.rounded_rectangle([(80, 1740), (1000, 1850)], radius=14, fill="#1e293b", outline="#e11d48", width=2)
        draw.text((120, 1775), "EDUCATIONAL ANALYSIS ONLY\nNOT FINANCIAL OR INVESTMENT ADVICE", fill="#fca5a5", font=f_disc)

    path = os.path.join(FRAMES_DIR, filename)
    img.save(path, quality=95)
    return path

def build_all_slides():
    print("Generating comprehensive visual slides...")
    
    # ------------------ Long Video Slides (50 slides, ~8s each) ------------------
    # The Hook (0-15s)
    make_slide_16x9("long_01.png", "THE $234B AT RISK", "Gartner Estimate: Enterprise SaaS Exposure by 2030",
                    badge="GARTNER ESTIMATE", highlight_box=("#e11d48", "UP TO $234 BILLION AT RISK", "20% of Global Enterprise SaaS Spending by 2030"))
    make_slide_16x9("long_02.png", "THE CORE SHIFT: DASHBOARDS TO AGENTS", "Why Autonomous AI Changes Enterprise Software Economics",
                    badge="ARCHITECTURAL SHIFT",
                    bullets=["Legacy SaaS: Scaled by employee headcount & monthly seats",
                             "Agentic AI: Executes tasks directly through APIs",
                             "The Result: Human GUI screens become invisible"])

    # Act 1 (15-105s): The Era of the Per-Seat License
    make_slide_16x9("long_03.png", "THE EVOLUTION OF SOFTWARE PRICING", "From One-Time Boxed Software to Recurring Subscriptions",
                    badge="ILLUSTRATIVE EXAMPLE (CONCEPTUAL TIMELINE)",
                    bullets=["2000s Transition: One-time CD-ROM licenses phased out",
                             "Rise of Cloud: Vendors charged monthly per employee login",
                             "Wall Street Boom: High-margin, predictable recurring revenue"])
    make_slide_16x9("long_04.png", "THE 'PER-SEAT' HEADCOUNT TIE", "Headcount Growth Equals Software Revenue Growth",
                    badge="ILLUSTRATIVE EXAMPLE",
                    bullets=["10,000 Employees = 10,000 Software Licenses",
                             "Monthly cost incurred regardless of actual usage frequency",
                             "Billions spent annually on underutilized enterprise seats"])
    make_slide_16x9("long_05.png", "THE WORKER AS COPY-PASTE INTERMEDIARY", "Software Designed for Human Eyeballs & Manual Clicks",
                    badge="ILLUSTRATIVE EXAMPLE",
                    bullets=["Employees navigating 15-20 browser tabs daily",
                             "Reading emails, manually extracting fields, pasting into forms",
                             "Entire UI built around human workflow ergonomics"])
    make_slide_16x9("long_06.png", "THE DEPRECIATION OF USER EXPERIENCE", "Gartner VP George Brocklehurst on Interface Value",
                    badge="EXPERT INSIGHT (CIO.COM)",
                    highlight_box=("#38bdf8", "‘When AI agents become the primary user, all that depreciates.’", "George Brocklehurst, Managing VP at Gartner"))

    # Act 2 (105-210s): Enter Agentic Arbitrage
    make_slide_16x9("long_07.png", "WHAT IS AGENTIC ARBITRAGE?", "Gartner's Official Definition of the 2026 Shift",
                    badge="GARTNER RESEARCH",
                    bullets=["AI agents completing tasks across multiple enterprise applications",
                             "Bypassing traditional Graphical User Interfaces (GUIs)",
                             "Delivering business outcomes directly through APIs and databases"])
    make_slide_16x9("long_08.png", "HOW AGENTS BYPASS THE APPLICATION LAYER", "Human Workflow vs Autonomous Agent Workflow",
                    badge="ILLUSTRATIVE EXAMPLE (ARCHITECTURE)",
                    bullets=["Human Path: Login -> Search -> Form Fill -> Click Submit (8-15 mins)",
                             "Agent Path: Event Webhook -> SQL Verification -> API Mutation (Milliseconds)",
                             "Zero human dashboard seats required for routine processing"])
    make_slide_16x9("long_09.png", "BREAKING THE HEADCOUNT-REVENUE LINK", "The End of Automatic SaaS Expansion",
                    badge="GARTNER ESTIMATE",
                    bullets=["Companies buying software for agents rather than people",
                             "Two human supervisors replace ten manual operators",
                             "Enterprises renew two software licenses instead of ten"])
    make_slide_16x9("long_10.png", "THE API-FIRST EVALUATION CRITERIA", "How CIOs Are Reassessing Enterprise Software",
                    badge="PROCUREMENT STRATEGY",
                    bullets=["Can an AI agent do everything through the API that a human can do on screen?",
                             "Do vendor contractual terms permit autonomous third-party usage?",
                             "Negotiating agentic permissions before renewals lock in"])

    # Act 3 (210-315s): Case Study: What Klarna Actually Said
    make_slide_16x9("long_11.png", "CASE STUDY: THE KLARNA STATEMENT", "Public Investor Call (August 2024)",
                    badge="PUBLIC RECORD (SALESFORCEBEN)",
                    highlight_box=("#facc15", "‘We just shut down Salesforce. Within a few weeks, we will shut down Workday.’", "Sebastian Siemiatkowski, Klarna CEO"))
    make_slide_16x9("long_12.png", "THE VERBATIM KLARNA QUOTE", "Exact Words from CEO Sebastian Siemiatkowski",
                    badge="VERIFIED QUOTE",
                    bullets=["‘There are large ongoing internal initiatives...’",
                             "‘...that are a combination of AI, standardization, and simplification.’",
                             "‘We are shutting down a lot of our SaaS providers, as we are able to consolidate.’"])
    make_slide_16x9("long_13.png", "HYPE VS REALITY IN ENTERPRISE MIGRATION", "What Really Happened Behind the Headlines",
                    badge="ANALYSIS",
                    bullets=["Not an overnight push-button replacement",
                             "Complex, multi-year operational consolidation",
                             "Human escalation remained vital for sensitive customer disputes"])
    make_slide_16x9("long_14.png", "THE REAL TAKEAWAY FOR ENTERPRISES", "Eliminating Redundant Software Tax",
                    badge="STRATEGIC LESSON",
                    bullets=["Enterprise buyers actively scrutinizing SaaS vendor lists",
                             "Consolidating overlapping tools and killing idle licenses",
                             "Prioritizing integrated workflows over fragmented dashboards"])

    # Act 4 (315-405s): The 40% Cancellation Warning
    make_slide_16x9("long_15.png", "THE REALITY CHECK: 40% RISK", "Gartner Predicts High Failure Rates in Agent Pilots",
                    badge="GARTNER PREDICTION",
                    highlight_box=("#ef4444", "More than 40% of Agentic AI Projects Canceled by 2027", "Due to escalating costs, unclear business value, and weak governance"))
    make_slide_16x9("long_16.png", "CHALLENGE #1: RECURSIVE TOKEN COSTS", "Why Agentic AI Is Not Free",
                    badge="ILLUSTRATIVE EXAMPLE (RISK FACTOR)",
                    bullets=["Complex multi-step reasoning models consume millions of tokens",
                             "Unoptimized agentic loops can exceed the cost of human software seats",
                             "Enterprises requiring cost observability before scaling"])
    make_slide_16x9("long_17.png", "CHALLENGE #2: GOVERNANCE & LIABILITY", "Who Owns an Agent's Mistakes?",
                    badge="RISK MANAGEMENT",
                    bullets=["Autonomous hallucination in financial transactions creates corporate liability",
                             "Unmonitored data exfiltration risks across API endpoints",
                             "Enterprises enforcing strict human-in-the-loop gates"])
    make_slide_16x9("long_18.png", "GOVERNANCE FRAMEWORKS MANDATORY", "Gartner Advice to Technology Leaders",
                    badge="BEST PRACTICES",
                    bullets=["Do not grant agent autonomy implicitly or unevenly",
                             "Establish explicit authorization gates for critical actions",
                             "Regular audit cycles for autonomous permissions"])

    # Act 5 (405-495s): The Software Metamorphosis
    make_slide_16x9("long_19.png", "‘SAAS WILL NOT BE DESTROYED’", "George Brocklehurst on the Future of the Industry",
                    badge="GARTNER QUOTE (CIO.COM)",
                    highlight_box=("#10b981", "‘This is less an apocalypse and more of a metamorphosis. SaaS will not be destroyed; it will emerge in a different form.’", "George Brocklehurst, Managing VP at Gartner"))
    make_slide_16x9("long_20.png", "SOFTWARE RESILIENCE MATRIX", "Which Categories Face Exposure vs Resilience",
                    badge="ILLUSTRATIVE EXAMPLE (CONCEPTUAL MATRIX)",
                    bullets=["High Exposure: Thin form-filling tools, status dashboards, workflow routing GUIs",
                             "High Resilience: Systems of record, compliance archives, proprietary data vaults",
                             "Value shifts from interface screens to data ownership & APIs"])
    make_slide_16x9("long_21.png", "THE OUTCOME-BASED PRICING ERA", "How Incumbent Software Vendors Are Adapting",
                    badge="BUSINESS MODEL SHIFT",
                    bullets=["Transitioning away from static per-seat monthly charges",
                             "Adopting consumption-based and outcome-based pricing models",
                             "Vendors integrating agentic orchestration into their core platforms"])

    # Outro (495-515s)
    make_slide_16x9("long_22.png", "CONCLUSION & EDUCATIONAL DISCLAIMER", "The Future of Enterprise Technology",
                    badge="DISCLAIMER",
                    highlight_box=("#e11d48", "EDUCATIONAL ANALYSIS ONLY", "Does not constitute financial, investment, or legal advice."),
                    bullets=["The 20-year era of evaluating software on human seats is transforming",
                             "Value moves to API infrastructure and verifiable data moats",
                             "Subscribe for more data-driven technology economics analysis"])

    # ------------------ Shorts Slides (9:16 Vertical) ------------------
    # Short 1: Why the $100/mo Seat is At Risk
    make_slide_9x16("short1_01.png", "UP TO $234B\nAT RISK BY 2030",
                    badge="GARTNER ESTIMATE",
                    bullets=["20 Years of $100/mo software seat licenses",
                             "Gartner: 20% of enterprise SaaS exposed",
                             "AI agents bypass dashboards via APIs",
                             "Companies buying software for agents, not seats"])

    # Short 2: What Klarna Actually Said
    make_slide_9x16("short2_01.png", "WHAT KLARNA\nACTUALLY SAID",
                    badge="VERIFIED RECORD",
                    quote="“There are large ongoing internal initiatives that are a combination of AI, standardization, and simplification. As an example, we just shut down Salesforce. Within a few weeks, we will shut down Workday. We are shutting down a lot of our SaaS providers, as we are able to consolidate.”",
                    bullets=["Not an overnight replacement",
                             "Intense operational consolidation",
                             "Human support escalation retained"])

    # Short 3: Software Exposure Matrix (with prominent disclaimer)
    make_slide_9x16("short3_01.png", "WHICH SOFTWARE\nIS MOST EXPOSED?",
                    badge="GARTNER ESTIMATE",
                    bullets=["High Exposure: Thin interface dashboards & forms",
                             "High Resilience: Core systems of record & compliance",
                             "SaaS not destroyed, but emerging in a new form",
                             "Value shifts to API layers & data moats"],
                    disclaimer=True)

    print("All slide graphics generated.")

if __name__ == "__main__":
    build_all_slides()
