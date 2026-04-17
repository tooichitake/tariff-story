"""Design system: colors, fonts, and layout constants."""
import os

# Paths — support both local dev and deployment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Try joined/ at project root first, then data/joined/
JOINED_DIR = os.path.join(BASE_DIR, "joined")
if not os.path.exists(JOINED_DIR):
    JOINED_DIR = os.path.join(BASE_DIR, "data", "joined")

REF_DIR = os.path.join(BASE_DIR, "reference")
if not os.path.exists(REF_DIR):
    REF_DIR = os.path.join(BASE_DIR, "data", "reference")

CLEANED_DIR = os.path.join(BASE_DIR, "cleaned")
if not os.path.exists(CLEANED_DIR):
    CLEANED_DIR = os.path.join(BASE_DIR, "data", "cleaned")

# =========================================================================
# COLOR_SEMANTICS — locked rules. Every chart / callout must comply.
# Rationale: a Phase 1 audit found three competing reds (#E74C3C, #C0392B,
# #FF8C00) doing different jobs, which diluted the narrative. Rule below:
#
#   Red    (#E74C3C)  → negative: burden, loss, cost, broken promise, danger
#   Green  (#2ECC71)  → positive: gain, kept promise, revenue, low impact
#   Amber  (#F5B041)  → accent:   highlight, callout, tariff-rate curve,
#                                   act banner, event filter (AA on #0E1117)
#   Blue   (#3498DB)  → neutral:  baselines, comparison groups, data series
#                                   with no emotional valence
#   Purple (#9B59B6)  → distinction (e.g. legal-impact events), sparing use
#
#   #C0392B (deep red) — deprecated except inside DECILE_COLORS gradient
#   #FF8C00 (orange)   — deprecated; replaced by COLORS["gold"]
# =========================================================================
COLORS = {
    "primary":    "#1B2838",   # Dark navy — authority
    "accent_red": "#E74C3C",   # NEGATIVE semantic (see COLOR_SEMANTICS)
    "accent_blue":"#3498DB",   # NEUTRAL data semantic
    "gold":       "#F5B041",   # ACCENT semantic — AA contrast on #0E1117
    "green":      "#2ECC71",   # POSITIVE semantic
    "purple":     "#9B59B6",   # DISTINCTION semantic
    "bg":         "#0E1117",   # Background
    "text":       "#FAFAFA",   # Text
    "muted":      "#7F8C8D",   # Muted text
}

# 10-decile gradient (deep red = highest burden → pale blue = lowest)
DECILE_COLORS = [
    "#C0392B",  # Decile 1 — darkest red
    "#E74C3C",  # Decile 2
    "#E67E22",  # Decile 3
    "#F39C12",  # Decile 4
    "#F1C40F",  # Decile 5
    "#D4AC0D",  # Decile 6
    "#2ECC71",  # Decile 7
    "#1ABC9C",  # Decile 8
    "#3498DB",  # Decile 9
    "#2980B9",  # Decile 10 — coolest blue
]

# Impact type colors for events
IMPACT_COLORS = {
    "tariff_up": "#E74C3C",
    "tariff_down": "#2ECC71",
    "retaliation": "#E67E22",
    "legal": "#9B59B6",
    "negotiation": "#3498DB",
    "threat": "#F39C12",
}

# Plotly chart template defaults (no height — set per chart)
CHART_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", size=13, color="#FAFAFA"),
    margin=dict(l=60, r=30, t=40, b=50),
    # Smooth transitions for any layout/data change
    transition=dict(duration=600, easing="cubic-in-out"),
)


def show_chart(fig, height=420):
    """Render a Plotly chart with correct Streamlit API (width='stretch')."""
    import streamlit as st
    fig.update_layout(height=height)
    st.plotly_chart(fig, width="stretch")
