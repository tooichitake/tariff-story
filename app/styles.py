"""CSS injection for narrative transitions, callout boxes, and typography.

Also exposes small Python helpers that emit ready-to-inject HTML for recurring
narrative components (act banners, insight boxes, visual anchors, sidebar
event cards, etc.). Components import these instead of duplicating markup.
"""
import os
import base64

# Absolute path to app/assets/ so image helpers resolve paths regardless of
# the caller's working directory. Streamlit Cloud runs from the repo root, so
# relative resolution is unreliable.
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

GLOBAL_CSS = """
<style>
/* ===== Global Typography ===== */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@300;400;500;600&display=swap');

.main .block-container {
    padding-top: 1rem;
    max-width: 1100px;
}

/* ===== Animations: Minimal — only for key emotional moments ===== */

/* Red danger pulse — countdown urgency */
@keyframes dangerPulse {
    0%, 100% { box-shadow: 0 0 8px rgba(231, 76, 60, 0.05); }
    50%      { box-shadow: 0 0 25px rgba(231, 76, 60, 0.3); }
}

/* Gentle breathing — hook headline only */
@keyframes breathe {
    0%, 100% { transform: scale(1); opacity: 0.95; }
    50%      { transform: scale(1.02); opacity: 1; }
}

/* ===== Act Transition Banners ===== */
.act-banner {
    background: linear-gradient(135deg, #1B2838 0%, #0E1117 100%);
    border-left: 4px solid #F5B041;
    padding: 2rem 2.5rem;
    margin: 3rem 0 2rem 0;
    border-radius: 0 8px 8px 0;
    /* clean, no animation */
}
.act-banner .act-number {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #F5B041;           /* WCAG AA-compliant on #0E1117 (5.5:1) */
    margin-bottom: 0.3rem;
}
.act-banner .act-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 2.2rem;
    font-weight: 900;
    color: #FAFAFA;
    margin-bottom: 0.5rem;
    line-height: 1.2;
}
.act-banner .act-question {
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    font-weight: 300;
    color: #7F8C8D;
    font-style: italic;
}

/* ===== Hook Section ===== */
.hook-container {
    text-align: center;
    padding: 4rem 2rem 3rem 2rem;
}
.hook-amount {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 5rem;
    font-weight: 900;
    color: #E74C3C;
    line-height: 1;
    margin-bottom: 0.5rem;
    /* Animation removed: the typographic weight already carries the emotion;
       pulsing the number made it feel less authoritative, not more. */
    text-shadow: 0 0 30px rgba(231, 76, 60, 0.3);
}
.hook-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 1.3rem;
    color: #7F8C8D;
    margin-bottom: 2rem;
}
.hook-question {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: #FAFAFA;
    margin-bottom: 1rem;
    text-shadow: 0 0 20px rgba(250, 250, 250, 0.15);
    /* Simplified: hook-amount already breathes; doubling the animation
       distracts from the intended hierarchy. */
}
.hook-scroll {
    font-size: 1rem;
    color: #7F8C8D;
    margin-top: 2rem;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 1; }
}

/* ===== Insight Callout Boxes ===== */
.insight-box {
    background: rgba(245, 176, 65, 0.08);
    border-left: 4px solid #F5B041;
    padding: 1.2rem 1.5rem;
    margin: 1.5rem 0;
    border-radius: 0 6px 6px 0;
    font-family: 'Inter', sans-serif;
    /* static border */
}
.insight-box .insight-label {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #F5B041;           /* WCAG AA-compliant on #0E1117 (5.5:1) */
    margin-bottom: 0.4rem;
}
.insight-box .insight-text {
    font-size: 1.05rem;
    color: #FAFAFA;
    line-height: 1.6;
}

/* ===== Transition Text ===== */
.transition-text {
    text-align: center;
    padding: 2rem 3rem;
    margin: 2rem 0;
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #7F8C8D;
    font-style: italic;
    border-top: 1px solid rgba(127, 140, 141, 0.2);
    border-bottom: 1px solid rgba(127, 140, 141, 0.2);
    /* static */
}

/* ===== Promise vs Verdict ===== */
.verdict-box {
    background: rgba(231, 76, 60, 0.06);
    border-left: 4px solid #E74C3C;
    padding: 1rem 1.5rem;
    margin: 1rem 0;
    border-radius: 0 6px 6px 0;
    /* static border */
}
.verdict-promise {
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #3498DB;
    margin-bottom: 0.2rem;
}
.verdict-result {
    font-size: 1.1rem;
    font-weight: 600;
    color: #E74C3C;
}

/* ===== Countdown Widget ===== */
.countdown {
    text-align: center;
    padding: 1.5rem;
    background: rgba(231, 76, 60, 0.08);
    border: 1px solid rgba(231, 76, 60, 0.3);
    border-radius: 8px;
    margin: 1rem 0;
    animation: dangerPulse 3s ease-in-out infinite;
}
.countdown .days {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 3.5rem;
    font-weight: 900;
    color: #E74C3C;
    line-height: 1;
    /* Inner breathing removed — the container's dangerPulse already carries
       urgency; layering two animations on the same widget reads as jitter. */
    text-shadow: 0 0 25px rgba(231, 76, 60, 0.4);
}
.countdown .label {
    font-size: 1rem;
    color: #7F8C8D;
    margin-top: 0.3rem;
}

/* ===== Declarative Chart Titles ===== */
.chart-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #FAFAFA;
    margin-bottom: 0.3rem;
}
.chart-subtitle {
    font-size: 0.85rem;
    color: #7F8C8D;
    margin-bottom: 1rem;
}

/* ===== Closing Address ===== */
.closing-address {
    text-align: center;
    padding: 3rem 2rem;
    margin: 2rem 0;
    border: 1px solid rgba(243, 156, 18, 0.3);
    border-radius: 8px;
    background: rgba(243, 156, 18, 0.05);
    /* static */
}
.closing-address .address-text {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.3rem;
    color: #FAFAFA;
    line-height: 1.8;
}

/* ===== Visual Anchor (hero bands with gradient + overlay text) ===== */
.visual-anchor {
    position: relative;
    overflow: hidden;
    border-radius: 10px;
    margin: 2rem 0 1.5rem 0;
    padding: 3.5rem 2.5rem;
    min-height: 260px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    background: #0E1117;
}
.visual-anchor.va-large { min-height: 360px; padding: 5rem 3rem; }
.visual-anchor .va-bg {
    position: absolute;
    inset: 0;
    background-size: cover;
    background-position: center;
    filter: brightness(0.85) contrast(1.05) saturate(0.9);
}
/* Heavier dark overlay when no image is present (pure CSS fallback needs
   the gradient to carry visual weight). Lighter overlay when there IS an
   image, so the photograph comes through. */
.visual-anchor .va-gradient {
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(14,17,23,0.92) 0%, rgba(14,17,23,0.70) 50%, rgba(14,17,23,0.92) 100%);
}
.visual-anchor.has-image .va-gradient {
    background: linear-gradient(90deg, rgba(14,17,23,0.80) 0%, rgba(14,17,23,0.35) 50%, rgba(14,17,23,0.55) 100%);
}
.visual-anchor .va-illustration {
    position: absolute;
    right: -40px;
    bottom: -40px;
    opacity: 0.07;
    color: #F5B041;
    pointer-events: none;
}
.visual-anchor .va-text {
    position: relative;
    z-index: 2;
    max-width: 75%;
}
.visual-anchor .va-eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #F5B041;
    margin-bottom: 0.8rem;
}
.visual-anchor .va-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 2.6rem;
    font-weight: 900;
    color: #FAFAFA;
    line-height: 1.1;
    margin-bottom: 0.8rem;
    text-shadow: 0 2px 12px rgba(0,0,0,0.6);
}
.visual-anchor.va-large .va-title { font-size: 3.4rem; }
.visual-anchor .va-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 1.15rem;
    color: #E0E0E0;
    line-height: 1.5;
    text-shadow: 0 1px 8px rgba(0,0,0,0.6);
}
.visual-anchor .va-attribution {
    position: absolute;
    bottom: 8px;
    right: 12px;
    z-index: 2;
    font-family: 'Inter', sans-serif;
    font-size: 0.65rem;
    color: rgba(250,250,250,0.45);
    letter-spacing: 0.5px;
}

/* ===== Sidebar event card (H3: event-filter thumbnail + narrative) ===== */
.event-card {
    margin-top: 0.5rem;
    padding: 0.8rem 0.9rem;
    background: rgba(243, 156, 18, 0.06);
    border-left: 3px solid #F5B041;
    border-radius: 0 6px 6px 0;
}
.event-card .event-thumb {
    width: 100%;
    max-height: 140px;
    object-fit: cover;
    border-radius: 4px;
    margin-bottom: 0.6rem;
    display: block;
}
.event-card .event-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.0rem;
    font-weight: 700;
    color: #FAFAFA;
    margin-bottom: 0.3rem;
    line-height: 1.25;
}
.event-card .event-meta {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    color: #F5B041;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.event-card .event-detail {
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    color: #C0C0C0;
    line-height: 1.5;
}
.event-card .event-source {
    font-size: 0.7rem;
    margin-top: 0.5rem;
}
.event-card .event-source a { color: #7F8C8D; text-decoration: none; }
.event-card .event-source a:hover { color: #F5B041; }

/* ===== 100-person pictogram (Act II closing visual) ===== */
.pictogram-wrap {
    margin: 1.5rem 0;
    padding: 1rem 1.2rem 1.5rem 1.2rem;
    background: rgba(27, 40, 56, 0.35);
    border: 1px solid rgba(127, 140, 141, 0.15);
    border-radius: 8px;
}
.pictogram-grid {
    display: grid;
    grid-template-columns: repeat(10, 1fr);
    gap: 4px;
    margin-top: 0.5rem;
}
.pictogram-col {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
}
.pictogram-col .decile-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.5px;
    color: #7F8C8D;
    margin-bottom: 4px;
}
.pictogram-col .decile-cost {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 0.85rem;
    font-weight: 700;
    color: #FAFAFA;
    margin-top: 4px;
}
.pictogram-col .dot-col {
    display: flex;
    flex-direction: column-reverse;
    gap: 2px;
    align-items: center;
}
.pictogram-col svg { display: block; }
.pictogram-caption {
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    color: #C0C0C0;
    line-height: 1.5;
    margin-top: 0.8rem;
}

/* ===== Promise vs Reality scorecard (Act III lead) ===== */
.scorecard {
    margin: 1.2rem 0 1.6rem 0;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid rgba(127, 140, 141, 0.2);
    background: rgba(27, 40, 56, 0.35);
}
.scorecard .sc-row {
    display: grid;
    grid-template-columns: 60px 1fr 1fr 140px;
    align-items: center;
    padding: 0.95rem 1.2rem;
    border-bottom: 1px solid rgba(127, 140, 141, 0.1);
    gap: 1rem;
}
.scorecard .sc-row:last-child { border-bottom: none; }
.scorecard .sc-icon { display:flex; align-items:center; justify-content:center; opacity: 0.8; }
.scorecard .sc-promise {
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    color: #C0C0C0;
    font-weight: 500;
}
.scorecard .sc-promise .sc-label {
    font-size: 0.7rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #3498DB;
    display:block;
    margin-bottom: 0.15rem;
}
.scorecard .sc-actual {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.05rem;
    color: #FAFAFA;
    font-weight: 600;
    line-height: 1.3;
}
.scorecard .sc-actual .sc-label {
    font-size: 0.7rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #F5B041;
    display:block;
    margin-bottom: 0.15rem;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
}
.scorecard .sc-verdict {
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 0.4rem 0.7rem;
    border-radius: 4px;
    text-align: center;
    white-space: nowrap;
}
.scorecard .sc-verdict.v-kept    { background: rgba(46, 204, 113, 0.15); color: #2ECC71; border: 1px solid rgba(46,204,113,0.3); }
.scorecard .sc-verdict.v-mixed   { background: rgba(243, 156, 18, 0.15); color: #F5B041; border: 1px solid rgba(243,156,18,0.3); }
.scorecard .sc-verdict.v-broken  { background: rgba(231, 76, 60, 0.12);  color: #E74C3C; border: 1px solid rgba(231,76,60,0.3); }

/* ===== Act intro drop cap ===== */
.act-intro::first-letter {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 3.5rem;
    font-weight: 900;
    color: #F5B041;
    float: left;
    line-height: 0.9;
    padding-right: 0.6rem;
    padding-top: 0.3rem;
}
.act-intro {
    font-family: 'Inter', sans-serif;
    font-size: 1.05rem;
    color: #E0E0E0;
    line-height: 1.7;
    margin: 1.2rem 0 1.8rem 0;
}

/* ===== Sidebar Styling ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0e14 0%, #0E1117 100%);
    border-right: 1px solid rgba(245, 176, 65, 0.12);
}
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0.8rem;
}
/* Tighten the default spacing between the radio/selectbox widgets we keep */
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    margin-bottom: 0.2rem;
}

/* Brand masthead at top of sidebar */
.sb-head {
    padding: 0.4rem 0 0.9rem 0;
    border-bottom: 1px solid rgba(245, 176, 65, 0.18);
    margin-bottom: 1.2rem;
}
.sb-head .sb-eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 0.62rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #F5B041;
    margin-bottom: 0.35rem;
}
.sb-head .sb-brand {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.35rem;
    font-weight: 900;
    color: #FAFAFA;
    line-height: 1.1;
    letter-spacing: 0.5px;
}
.sb-head .sb-tag {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 0.85rem;
    font-style: italic;
    color: #7F8C8D;
    margin-top: 0.3rem;
}

/* Small uppercase section label (gold chip style) */
.sb-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #F5B041;
    margin: 1.2rem 0 0.7rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px dotted rgba(245, 176, 65, 0.22);
}

/* Table-of-contents list */
.sb-nav {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
    margin-bottom: 1rem;
}
.sb-nav a {
    display: grid;
    grid-template-columns: 38px 1fr;
    align-items: center;
    gap: 0.6rem;
    padding: 0.55rem 0.6rem;
    border-radius: 4px;
    text-decoration: none !important;
    color: #E0E0E0 !important;
    border-left: 2px solid transparent;
    transition: background 0.15s ease, border-color 0.15s ease, transform 0.15s ease;
}
.sb-nav a:hover {
    background: rgba(245, 176, 65, 0.08);
    border-left: 2px solid #F5B041;
    transform: translateX(2px);
    color: #FAFAFA !important;
}
.sb-nav .sb-roman {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.05rem;
    font-weight: 900;
    color: #F5B041;
    text-align: center;
    line-height: 1;
}
.sb-nav .sb-opening .sb-roman { font-size: 0.62rem; letter-spacing: 1.5px; }
.sb-nav .sb-title {
    font-family: 'Inter', sans-serif;
    font-size: 0.88rem;
    font-weight: 500;
    line-height: 1.25;
}
.sb-nav .sb-question {
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    color: #7F8C8D;
    margin-top: 0.1rem;
    font-style: italic;
}

/* Footer block (data + course credits) */
.sb-foot {
    margin-top: 1.5rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(127, 140, 141, 0.15);
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    color: #7F8C8D;
    line-height: 1.55;
}
.sb-foot .sb-foot-row + .sb-foot-row {
    margin-top: 0.35rem;
}
.sb-foot strong { color: #C0C0C0; font-weight: 500; }
.sb-foot .sb-dot {
    display: inline-block;
    width: 3px; height: 3px;
    border-radius: 50%;
    background: #F5B041;
    margin: 0 0.4rem;
    vertical-align: middle;
    opacity: 0.7;
}

/* ===== Metric overrides ===== */
[data-testid="stMetric"] {
    background: rgba(27, 40, 56, 0.5);
    border: 1px solid rgba(127, 140, 141, 0.15);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    /* static */
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 6px 20px rgba(243, 156, 18, 0.2);
    animation-play-state: paused;
}
</style>
"""


def act_banner(act_num: str, title: str, question: str) -> str:
    return f"""
    <div class="act-banner">
        <div class="act-number">Act {act_num}</div>
        <div class="act-title">{title}</div>
        <div class="act-question">{question}</div>
    </div>
    """


def insight_box(text: str) -> str:
    return f"""
    <div class="insight-box">
        <div class="insight-label">Key Insight</div>
        <div class="insight-text">{text}</div>
    </div>
    """


def transition_text(text: str) -> str:
    return f'<div class="transition-text">{text}</div>'


def verdict_box(promise: str, result: str) -> str:
    return f"""
    <div class="verdict-box">
        <div class="verdict-promise">Promise: {promise}</div>
        <div class="verdict-result">Verdict: {result}</div>
    </div>
    """


def chart_header(title: str, subtitle: str = "") -> str:
    sub = f'<div class="chart-subtitle">{subtitle}</div>' if subtitle else ""
    return f'<div class="chart-title">{title}</div>{sub}'


def countdown_widget(days: int) -> str:
    return f"""
    <div class="countdown">
        <div class="days">{days}</div>
        <div class="label">days until Section 122 expires</div>
    </div>
    """


def closing_address(text: str) -> str:
    return f"""
    <div class="closing-address">
        <div class="address-text">{text}</div>
    </div>
    """


# =========================================================================
# Visual anchors (hero bands with real imagery or CSS illustration fallback)
# =========================================================================

# Lucide-style SVG icons. Simplified open-source iconography (MIT-equivalent).
# Used as (a) fallback illustrations for visual anchors when images are
# absent, and (b) inline product-category icons in Act II viz4.
# Attribution is in app/assets/images/LICENSE.md.
_LUCIDE_SVG = {
    "shopping-cart": """<svg xmlns="http://www.w3.org/2000/svg" width="360" height="360" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></svg>""",
    "hand-coins": """<svg xmlns="http://www.w3.org/2000/svg" width="360" height="360" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 15h2a2 2 0 1 0 0-4h-3c-.6 0-1.1.2-1.4.6L3 17"/><path d="m7 21 1.6-1.4c.3-.4.8-.6 1.4-.6h4c1.1 0 2.1-.4 2.8-1.2l4.6-4.4a2 2 0 0 0-2.75-2.91l-4.2 3.9"/><path d="m2 16 6 6"/><circle cx="16" cy="9" r="2.9"/><circle cx="6" cy="5" r="3"/></svg>""",
    "scale": """<svg xmlns="http://www.w3.org/2000/svg" width="360" height="360" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/></svg>""",
    "columns": """<svg xmlns="http://www.w3.org/2000/svg" width="360" height="360" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 21h10"/><path d="M6 21v-9"/><path d="M18 21v-9"/><path d="M9 21V12"/><path d="M15 21V12"/><path d="M12 21V12"/><path d="M3 10h18l-3-6H6l-3 6Z"/></svg>""",
    "shirt": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.38 3.46 16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"/></svg>""",
    "footprints": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 16v-2.38C4 11.5 2.97 10.5 3 8c.03-2.72 1.49-6 4.5-6C9.37 2 10 3.8 10 5.5c0 3.11-2 5.66-2 8.68V16a2 2 0 1 1-4 0Z"/><path d="M20 20v-2.38c0-2.12 1.03-3.12 1-5.62-.03-2.72-1.49-6-4.5-6C14.63 6 14 7.8 14 9.5c0 3.11 2 5.66 2 8.68V20a2 2 0 1 0 4 0Z"/><path d="M16 17h4"/><path d="M4 13h4"/></svg>""",
    "toy-brick": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="12" x="3" y="8" rx="1"/><path d="M10 8V5c0-.6-.4-1-1-1H6a1 1 0 0 0-1 1v3"/><path d="M19 8V5c0-.6-.4-1-1-1h-3a1 1 0 0 0-1 1v3"/></svg>""",
    "apple": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20.94c1.5 0 2.75 1.06 4 1.06 3 0 6-8 6-12.22A4.91 4.91 0 0 0 17 5c-2.22 0-4 1.44-5 2-1-.56-2.78-2-5-2a4.9 4.9 0 0 0-5 4.78C2 14 5 22 8 22c1.25 0 2.5-1.06 4-1.06Z"/><path d="M10 2c1 .5 2 2 2 5"/></svg>""",
    "smartphone": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/></svg>""",
    "sofa": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 9V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v3"/><path d="M2 11v5a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-5a2 2 0 0 0-4 0v2H6v-2a2 2 0 0 0-4 0Z"/><path d="M4 18v2"/><path d="M20 18v2"/><path d="M12 4v9"/></svg>""",
    "car": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9L18 10.4c-.5-.9-1-2-2-3l-2-3H4l-2 3L2 10l-1 1v5c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/></svg>""",
    "cog": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20a8 8 0 1 0 0-16 8 8 0 0 0 0 16Z"/><circle cx="12" cy="12" r="3"/></svg>""",
    "pill": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/></svg>""",
    "user": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>""",
    "hammer": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 12-8.5 8.5c-.83.83-2.17.83-3 0 0 0 0 0 0 0a2.12 2.12 0 0 1 0-3L12 9"/><path d="M17.64 15 22 10.64"/><path d="m20.91 11.7-1.25-1.25c-.6-.6-.93-1.4-.93-2.25v-.86L16.01 4.6a5.56 5.56 0 0 0-3.94-1.64H9l.92.82A6.18 6.18 0 0 1 12 8.4v1.56l2 2h2.47l2.26 1.91"/></svg>""",
    "tree-pine": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m17 14 3 3.3a1 1 0 0 1-.7 1.7H4.7a1 1 0 0 1-.7-1.7L7 14h-.3a1 1 0 0 1-.7-1.7L9 9h-.2A1 1 0 0 1 8 7.3L12 3l4 4.3a1 1 0 0 1-.8 1.7H15l3 3.3a1 1 0 0 1-.7 1.7H17Z"/><path d="M12 22v-3"/></svg>""",
    "flask-conical": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 2v7.527a2 2 0 0 1-.211.896L4.72 20.55a1 1 0 0 0 .9 1.45h12.76a1 1 0 0 0 .9-1.45l-5.069-10.127A2 2 0 0 1 14 9.527V2"/><path d="M8.5 2h7"/><path d="M7 16h10"/></svg>""",
    "cpu": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>""",
    "utensils": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/></svg>""",
    "truck": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/></svg>""",
    "anvil": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 10H6a4 4 0 0 1-4-4 1 1 0 0 1 1-1h4"/><path d="M7 5a1 1 0 0 1 1-1h13a1 1 0 0 1 1 1 7 7 0 0 1-7 7H8a1 1 0 0 1-1-1z"/><path d="M9 12v5"/><path d="M15 12v5"/><path d="M5 20a3 3 0 0 1 3-3h8a3 3 0 0 1 3 3 1 1 0 0 1-1 1H6a1 1 0 0 1-1-1z"/></svg>""",
    "pickaxe": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.531 12.469 6.619 20.38a1 1 0 1 1-3-3l7.912-7.912"/><path d="M15.686 4.314A12.5 12.5 0 0 0 5.461 2.958 1 1 0 0 0 5.58 4.71a22 22 0 0 1 6.318 3.393"/><path d="M17.7 3.7a1 1 0 0 0-1.4 0l-4.6 4.6a1 1 0 0 0 0 1.4l2.6 2.6a1 1 0 0 0 1.4 0l4.6-4.6a1 1 0 0 0 0-1.4Z"/><path d="M19.686 8.314a12.501 12.501 0 0 1 1.356 10.225 1 1 0 0 1-1.751-.119 22 22 0 0 0-3.393-6.319"/></svg>""",
    "scissors": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><path d="M8.12 8.12 12 12"/><path d="M20 4 8.12 15.88"/><circle cx="6" cy="18" r="3"/><path d="M14.8 14.8 20 20"/></svg>""",
}

CATEGORY_ICONS = {
    # Consumer retail (original keys — keep for any chart that uses them)
    "Apparel":                "shirt",
    "Footwear":               "footprints",
    "Toys & Games":           "toy-brick",
    "Household Textiles":     "shirt",
    "Consumer Electronics":   "smartphone",
    "Furniture":              "sofa",
    "Auto Parts":             "car",
    "Fresh Food":             "apple",
    "Machinery":              "cog",
    "Pharmaceuticals":        "pill",

    # Industry/sectoral keys (Yale Budget Lab commodity-price categories —
    # these are what commodity_prices CSV actually ships). Each of the 10
    # rows visible in Act II viz4 maps to a semantically distinct icon.
    "Textiles":               "scissors",       # tailoring / fabric cutting
    "Metal products":         "anvil",          # forged/finished metal
    "Metals nec":             "pickaxe",        # raw/extracted metals
    "Motor vehicles":         "car",
    "Electronic equipment":   "cpu",
    "Machinery":              "cog",            # keep override
    "Wood products":          "tree-pine",
    "Chemical products":      "flask-conical",
    "Food products":          "utensils",
    # Extra industry keys (may appear in future data refreshes; each remains
    # distinct from the ten active rows above).
    "Transport equipment":    "truck",
    "Mineral products":       "pickaxe",
    "Leather products":       "footprints",
    "Petroleum":              "flask-conical",
    "Plastic products":       "flask-conical",
    "Paper products":         "tree-pine",
    "Rubber products":        "flask-conical",
    "Other manufactures":     "cog",
}


def _image_to_data_uri(path: str) -> str:
    """Read a local image and return an inline data URI. Empty string if missing."""
    if not path or not os.path.isfile(path):
        return ""
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    mime = {"webp": "image/webp", "jpg": "image/jpeg", "jpeg": "image/jpeg",
            "png": "image/png", "gif": "image/gif"}.get(ext, "image/jpeg")
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def visual_anchor(
    title: str,
    subtitle: str = "",
    image_path: str = "",
    eyebrow: str = "",
    icon: str = "shopping-cart",
    large: bool = False,
    attribution: str = "",
    assets_root: str = "",
) -> str:
    """Render a narrative visual anchor (hero band) with graceful fallback.

    When ``image_path`` resolves to an existing file, the band displays that
    image behind a dark gradient + overlay text. When the file is absent, the
    band falls back to a CSS-only illustration: a gradient background with a
    large low-opacity SVG icon (``icon``) in the corner. Either way the band
    has the same dimensions and typography, so layout doesn't shift when
    imagery is added later.

    Args:
        title: Main overlay headline (Playfair Display).
        subtitle: Sub-headline (Inter, 1.15rem).
        image_path: Relative path from ``assets_root`` to a local image. If
            the file doesn't exist, CSS illustration fallback is used.
        eyebrow: Small uppercase tag above the title.
        icon: Key into ``_LUCIDE_SVG`` for the illustration fallback.
        large: If True, uses taller layout + larger title (for H1 Hook).
        attribution: Photo credit string shown bottom-right (only when image
            is present).
        assets_root: Directory to resolve ``image_path`` against.
    """
    # Build the HTML as a flat string (no newlines + no indentation) so
    # Streamlit's markdown pass doesn't mistake blank-looking indented lines
    # — which appear when optional template variables like ``image_path`` or
    # ``attribution`` are empty — for 4-space-indented code blocks.
    classes = "visual-anchor" + (" va-large" if large else "")
    resolved = os.path.join(assets_root, image_path) if (assets_root and image_path) else image_path
    data_uri = _image_to_data_uri(resolved) if image_path else ""
    if data_uri:
        classes += " has-image"   # triggers lighter gradient so photo shows through

    parts = [f'<div class="{classes}">']
    if data_uri:
        parts.append(f'<div class="va-bg" style="background-image: url(\'{data_uri}\');"></div>')
    parts.append('<div class="va-gradient"></div>')
    if not data_uri:
        svg = _LUCIDE_SVG.get(icon, _LUCIDE_SVG["shopping-cart"])
        parts.append(f'<div class="va-illustration">{svg}</div>')

    text_parts = ['<div class="va-text">']
    if eyebrow:
        text_parts.append(f'<div class="va-eyebrow">{eyebrow}</div>')
    text_parts.append(f'<div class="va-title">{title}</div>')
    if subtitle:
        text_parts.append(f'<div class="va-subtitle">{subtitle}</div>')
    text_parts.append('</div>')
    parts.append("".join(text_parts))

    if data_uri and attribution:
        parts.append(f'<div class="va-attribution">{attribution}</div>')

    parts.append('</div>')
    return "".join(parts)


def event_card(
    event_short: str,
    event_detail: str,
    event_date: str,
    tariff_rate: float,
    image_path: str = "",
    source_url: str = "",
    assets_root: str = "",
) -> str:
    """Render the sidebar event card when a user selects an event.

    If ``image_path`` resolves to a file, shows it as a thumbnail. Otherwise
    the card still renders with title/meta/detail — the image is optional
    polish, not load-bearing.
    """
    # Flat single-line HTML — see visual_anchor() for rationale.
    resolved = os.path.join(assets_root, image_path) if (assets_root and image_path) else image_path
    data_uri = _image_to_data_uri(resolved) if image_path else ""
    parts = ['<div class="event-card">']
    if data_uri:
        parts.append(f'<img class="event-thumb" src="{data_uri}" alt="{event_short}">')
    parts.append(f'<div class="event-meta">{event_date} · Tariff {tariff_rate:.1f}%</div>')
    parts.append(f'<div class="event-title">{event_short}</div>')
    parts.append(f'<div class="event-detail">{event_detail}</div>')
    if source_url:
        parts.append(
            f'<div class="event-source"><a href="{source_url}" target="_blank" '
            f'rel="noopener">Source \u2197</a></div>'
        )
    parts.append('</div>')
    return "".join(parts)


def act_intro(text: str) -> str:
    """Render an Act introduction paragraph with drop-cap first letter."""
    return f'<p class="act-intro">{text}</p>'


def pictogram_100(decile_data, decile_colors) -> str:
    """Render a 10×10 person pictogram for Act II.

    The chart represents 100 Americans: 10 per income decile (column). Each
    person icon in a column is rendered in the decile's colour, with the
    annual USD cost of tariffs shown beneath the column. Visual metaphor:
    *same country, different tax*.

    Args:
        decile_data: list of (decile_label:str, usd_cost:float) tuples, in
            decile order (1..10 from left to right).
        decile_colors: list of 10 CSS colour strings parallel to ``decile_data``.
    """
    user_svg = _LUCIDE_SVG["user"]
    cols = []
    for (label, cost), color in zip(decile_data, decile_colors):
        svg = user_svg.replace('fill="currentColor"', f'fill="{color}"')
        dots = "".join(svg for _ in range(10))
        cols.append(
            f'<div class="pictogram-col">'
            f'<div class="decile-label">{label}</div>'
            f'<div class="dot-col">{dots}</div>'
            f'<div class="decile-cost">${cost:,.0f}</div>'
            f'</div>'
        )
    # Flat HTML — see visual_anchor() for the Streamlit-markdown rationale.
    caption = (
        "One hundred Americans, grouped by income decile. Colour intensity "
        "and the dollar figure underneath each group show the annual tariff "
        "tax paid by a household in that decile. Same country, different tax."
    )
    return (
        '<div class="pictogram-wrap">'
        f'<div class="pictogram-grid">{"".join(cols)}</div>'
        f'<div class="pictogram-caption">{caption}</div>'
        '</div>'
    )


def scorecard(rows) -> str:
    """Render a Promise vs Reality scorecard grid.

    Each item in ``rows`` is a dict with keys:
        icon: key into ``_LUCIDE_SVG`` (e.g. "scale", "cog").
        promise: the original promise text (one sentence).
        actual: the observed outcome text (one sentence or number).
        verdict: one of "kept", "mixed", "broken" — drives the pill color.
        verdict_text: display text for the verdict pill (e.g. "Broken").

    The scorecard is the leading visual in Act III: readers should be able to
    understand whether each tariff promise was kept before any chart loads.
    """
    html_rows = []
    for r in rows:
        icon_svg = _LUCIDE_SVG.get(r.get("icon", "cog"), _LUCIDE_SVG["cog"])
        # Downsize the icon for in-row use.
        icon_svg = (icon_svg
                    .replace('width="360"', 'width="32"')
                    .replace('height="360"', 'height="32"')
                    .replace('width="24"', 'width="32"')
                    .replace('height="24"', 'height="32"')
                    .replace('stroke="currentColor"', 'stroke="#F5B041"'))
        v = r.get("verdict", "mixed")
        v_class = {"kept": "v-kept", "mixed": "v-mixed", "broken": "v-broken"}.get(v, "v-mixed")
        v_text = r.get("verdict_text", v.title())
        html_rows.append(
            f'<div class="sc-row">'
            f'<div class="sc-icon">{icon_svg}</div>'
            f'<div class="sc-promise"><span class="sc-label">Promise</span>{r["promise"]}</div>'
            f'<div class="sc-actual"><span class="sc-label">Reality</span>{r["actual"]}</div>'
            f'<div class="sc-verdict {v_class}">{v_text}</div>'
            f'</div>'
        )
    return f'<div class="scorecard">{"".join(html_rows)}</div>'


def category_icon_svg(category: str, size: int = 18, color: str = "#F5B041") -> str:
    """Return inline SVG markup for a product category icon (Act II viz4).

    Unknown categories fall back to the generic ``columns`` icon so the chart
    still renders consistently.
    """
    key = CATEGORY_ICONS.get(category, "columns")
    raw = _LUCIDE_SVG.get(key, _LUCIDE_SVG["columns"])
    # Size the SVG and color it for inline use in chart labels.
    return (raw
            .replace('width="24"', f'width="{size}"')
            .replace('height="24"', f'height="{size}"')
            .replace('width="360"', f'width="{size}"')
            .replace('height="360"', f'height="{size}"')
            .replace('stroke="currentColor"', f'stroke="{color}"'))


# =========================================================================
# Plotly event annotation + highlight helpers
# Extracted from act1/act3/act4 where similar code was duplicated. Reused
# in all acts so a design change propagates from one place.
# =========================================================================

def highlight_event_window(
    fig,
    event_date,
    window_days: int = 14,
    color: str = "#F5B041",
    opacity: float = 0.08,
    line_color: str = "#F5B041",
):
    """Add a vertical band + centerline around ``event_date`` to a Plotly figure.

    The band spans ``±window_days`` around the event. Use this instead of a
    bare ``add_vline`` when you want viewers to feel the event's window of
    influence, not just its instant.
    """
    import pandas as pd
    if event_date is None:
        return fig
    d = pd.to_datetime(event_date)
    delta = pd.Timedelta(days=int(window_days))
    fig.add_vrect(
        x0=d - delta, x1=d + delta,
        fillcolor=color, opacity=opacity,
        layer="below", line_width=0,
    )
    fig.add_vline(
        x=d, line=dict(color=line_color, width=2, dash="dot"),
    )
    return fig


def annotate_event(fig, event_row, y=None, text_size: int = 10, color: str = "#F5B041"):
    """Pin a small event label at the top of the plot area for ``event_row``.

    ``event_row`` is a pandas Series with at least ``date`` and
    ``event_short`` fields (as produced by ``load_key_events()``).
    """
    import pandas as pd
    d = pd.to_datetime(event_row["date"])
    fig.add_annotation(
        x=d, y=y if y is not None else 1.0,
        yref="paper" if y is None else "y",
        text=f"<b>{event_row['event_short']}</b>",
        showarrow=False,
        font=dict(size=text_size, color=color),
        bgcolor="rgba(14,17,23,0.85)",
        borderpad=3,
        xanchor="center", yanchor="bottom",
    )
    return fig


_metric_counter = 0


def styled_metric_card(border_color: str = "#F5B041"):
    """Return a st.container with CSS targeting via key (new Streamlit API)."""
    import streamlit as st
    global _metric_counter
    _metric_counter += 1
    key = f"smc_{_metric_counter}"
    # Inject scoped CSS for this container's key
    st.markdown(f"""
    <style>
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"]:has(> div[data-testid="element-container"] > div[key="{key}"]) {{
        background: linear-gradient(135deg, rgba(27,40,56,0.6) 0%, rgba(14,17,23,0.8) 100%);
        border: 1px solid rgba(127,140,141,0.15);
        border-top: 3px solid {border_color};
        border-radius: 8px;
        padding: 0.6rem 1rem;
    }}
    </style>
    """, unsafe_allow_html=True)
    return st.container(key=key)
