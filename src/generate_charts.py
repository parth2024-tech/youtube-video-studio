#!/usr/bin/env python3
"""
Chart and Diagram Generator for Autonomous YouTube Studio
Strictly enforces Rule #3:
- Only verified data is cited to real sources.
- Conceptual and architectural diagrams are prominently labeled 'ILLUSTRATIVE EXAMPLE' with NO source attribution.
- All unverified synthetic figures ($936B, 85/45/15, 42ms, $0.002, 10,000 seats) are completely removed.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

def generate_all_charts(output_dir="output/saaspocalypse-ai-agents/charts"):
    os.makedirs(output_dir, exist_ok=True)

    # -------------------------------------------------------------
    # Scene 1: Conceptual Evolution of SaaS Business Models (ILLUSTRATIVE)
    # Labeled: ILLUSTRATIVE EXAMPLE (NO SOURCE ATTRIBUTION)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
    fig.patch.set_facecolor("#0b0f19")
    ax.set_facecolor("#0b0f19")

    stages = [
        "Phase 1: On-Premise\n(One-Time CD Box)",
        "Phase 2: Cloud SaaS\n(Per-Seat Monthly Fee)",
        "Phase 3: Agentic AI\n(Outcome & API Usage)"
    ]
    y_pos = [1, 2, 3]

    # Clean conceptual timeline blocks
    ax.barh(y_pos, [1, 2, 3], color=["#475569", "#38bdf8", "#00e5ff"], height=0.45)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(stages, color="#ffffff", fontsize=16, weight="bold")
    ax.set_xticks([])
    
    # Prominent Illustrative Example label (NO SOURCE NAME)
    ax.text(0.02, 0.95, "ILLUSTRATIVE EXAMPLE (CONCEPTUAL TIMELINE)", transform=ax.transAxes,
            color="#facc15", fontsize=15, weight="bold",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#1e293b", edgecolor="#facc15", alpha=0.9))

    ax.set_title("THE EVOLUTION OF SOFTWARE MONETIZATION\nFrom Fixed Licenses to Per-Seat Subscriptions to Autonomous Outcomes",
                 color="#ffffff", fontsize=22, pad=25, weight="bold")
    
    # Subtext explaining each phase
    ax.text(1.05, 1, "Fixed asset, no recurring fee", color="#94a3b8", fontsize=14, va="center")
    ax.text(2.05, 2, "Recurring monthly fee per employee login", color="#94a3b8", fontsize=14, va="center")
    ax.text(3.05, 3, "Workflows executed directly via APIs", color="#38bdf8", fontsize=14, va="center")

    ax.set_xlim(0, 4.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_color("#334155")

    plt.tight_layout()
    chart1_path = os.path.join(output_dir, "scene1_evolution.png")
    plt.savefig(chart1_path)
    plt.close()
    print(f"Generated {chart1_path}")

    # -------------------------------------------------------------
    # Scene 2: Verified Gartner Estimate ($234B & 20% Share)
    # Cites Gartner estimate properly
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
    fig.patch.set_facecolor("#0b0f19")
    ax.set_facecolor("#0b0f19")

    # Showing verified 20% proportion from Gartner July 1, 2026 forecast
    proportions = [20, 80]
    labels = [
        "Exposed to Agentic Arbitrage\n(Gartner estimate: Up to $234 Billion)",
        "Remaining Enterprise\nSoftware Spending"
    ]
    colors = ["#e11d48", "#1e293b"]

    wedges, texts, autotexts = ax.pie(
        proportions,
        labels=labels,
        autopct="%1.0f%%",
        startangle=140,
        colors=colors,
        explode=(0.08, 0),
        textprops=dict(color="#ffffff", fontsize=16, weight="bold"),
        wedgeprops=dict(width=0.45, edgecolor="#0b0f19", linewidth=3)
    )

    for autotext in autotexts:
        autotext.set_color("#ffffff")
        autotext.set_fontsize(22)
        autotext.set_weight("bold")

    ax.set_title("GARTNER ESTIMATE: 20% OF ENTERPRISE SaaS EXPOSED BY 2030\nUp to $234 Billion at Risk from Autonomous AI Arbitrage",
                 color="#ffffff", fontsize=22, pad=30, weight="bold")
    
    # Institutional attribution
    ax.text(0.5, -0.05, "Source: Gartner Research (SaaSpocalypse / Agentic Arbitrage Forecast)",
            transform=ax.transAxes, color="#94a3b8", fontsize=13, ha="center")

    plt.tight_layout()
    chart2_path = os.path.join(output_dir, "scene2_gartner_share.png")
    plt.savefig(chart2_path)
    plt.close()
    print(f"Generated {chart2_path}")

    # -------------------------------------------------------------
    # Scene 3: Architectural Comparison (ILLUSTRATIVE EXAMPLE)
    # Labeled: ILLUSTRATIVE EXAMPLE (NO SOURCE ATTRIBUTION)
    # Zero fabricated metrics (no 42ms, no $0.002, no $45-$65/hr)
    # -------------------------------------------------------------
    img3 = Image.new("RGB", (1600, 900), color="#0b0f19")
    d3 = ImageDraw.Draw(img3)

    font_path = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"
    if not os.path.exists(font_path):
        font_path = "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Bold.ttf"

    f_title = ImageFont.truetype(font_path, 40)
    f_badge = ImageFont.truetype(font_path, 22)
    f_h2 = ImageFont.truetype(font_path, 30)
    f_p = ImageFont.truetype(font_path, 24)

    # Title
    d3.text((380, 40), "HOW AGENTIC ARBITRAGE WORKS", fill="#ffffff", font=f_title)
    
    # Prominent Illustrative Example badge
    d3.rounded_rectangle([(80, 40), (330, 85)], radius=8, fill="#1e293b", outline="#facc15", width=2)
    d3.text((95, 50), "ILLUSTRATIVE EXAMPLE", fill="#facc15", font=f_badge)

    # Left Box: Traditional GUI Workflow
    d3.rounded_rectangle([(100, 130), (760, 800)], radius=16, fill="#111827", outline="#ef4444", width=2)
    d3.text((140, 165), "TRADITIONAL: HUMAN DASHBOARD", fill="#ef4444", font=f_h2)
    
    steps_left = [
        "1. Human user logs into web application",
        "2. Reads incoming document / ticket manually",
        "3. Manually navigates multiple UI screens",
        "4. Copies & pastes data across forms",
        "5. Clicks submit buttons to update system",
        "",
        "Key Dependency: Human interaction with GUI",
        "Licensing Model: Monthly fee per employee seat"
    ]
    y = 240
    for s in steps_left:
        color = "#f87171" if "Key Dependency" in s or "Licensing" in s else "#cbd5e1"
        d3.text((140, y), s, fill=color, font=f_p)
        y += 55

    # Right Box: Agentic API Workflow
    d3.rounded_rectangle([(840, 130), (1500, 800)], radius=16, fill="#0c1a2e", outline="#00e5ff", width=2)
    d3.text((880, 165), "NEW: AUTONOMOUS AGENT API", fill="#00e5ff", font=f_h2)

    steps_right = [
        "1. Event trigger / API webhook fires directly",
        "2. AI agent reads data schema autonomously",
        "3. Verifies logic across internal databases",
        "4. Executes cross-system updates via API",
        "5. Completes transaction without opening GUI",
        "",
        "Key Advantage: GUI dashboard is bypassed",
        "Licensing Model: Outcome & consumption pricing"
    ]
    y = 240
    for s in steps_right:
        color = "#38bdf8" if "Key Advantage" in s or "Licensing" in s else "#e2e8f0"
        d3.text((880, y), s, fill=color, font=f_p)
        y += 55

    chart3_path = os.path.join(output_dir, "scene3_workflow_comparison.png")
    img3.save(chart3_path)
    print(f"Generated {chart3_path}")

    # -------------------------------------------------------------
    # Scene 4: Software Exposure Matrix (ILLUSTRATIVE CATEGORIES)
    # Labeled: ILLUSTRATIVE EXAMPLE (NO SOURCE ATTRIBUTION)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
    fig.patch.set_facecolor("#0b0f19")
    ax.set_facecolor("#0b0f19")

    ax.text(0.02, 0.95, "ILLUSTRATIVE EXAMPLE (CONCEPTUAL MATRIX)", transform=ax.transAxes,
            color="#facc15", fontsize=15, weight="bold",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#1e293b", edgecolor="#facc15", alpha=0.9))

    ax.set_title("ENTERPRISE SOFTWARE RESILIENCE MATRIX\nHigh Exposure (Thin Interfaces) vs High Resilience (Systems of Record)",
                 color="#ffffff", fontsize=22, pad=25, weight="bold")

    # Draw 2 columns
    col1 = [
        "• Thin Form-Filling Dashboards",
        "• Basic Workflow Routing GUIs",
        "• Manual Data-Aggregation Tools",
        "• Simple Ticketing Portals"
    ]
    col2 = [
        "• Proprietary Transaction Ledgers",
        "• Core Banking & ERP Backends",
        "• Regulatory & Compliance Vaults",
        "• Secure API Infrastructure"
    ]

    ax.text(0.25, 0.75, "HIGH EXPOSURE\n(Bypassed by AI Agents)", color="#ef4444", fontsize=18, weight="bold", ha="center")
    y = 0.60
    for item in col1:
        ax.text(0.08, y, item, color="#cbd5e1", fontsize=15)
        y -= 0.08

    ax.text(0.75, 0.75, "HIGH RESILIENCE\n(Connected to by AI Agents)", color="#00e5ff", fontsize=18, weight="bold", ha="center")
    y = 0.60
    for item in col2:
        ax.text(0.58, y, item, color="#e2e8f0", fontsize=15)
        y -= 0.08

    # Dividing line
    ax.axvline(0.5, color="#334155", linestyle="--", linewidth=2)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.9)
    ax.axis("off")

    plt.tight_layout()
    chart4_path = os.path.join(output_dir, "scene4_resilience_matrix.png")
    plt.savefig(chart4_path)
    plt.close()
    print(f"Generated {chart4_path}")

if __name__ == "__main__":
    generate_all_charts()
