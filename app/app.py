"""
The Tariff Tax: Who Pays?
A data narrative on Trump's 2025 Tariff War.

Narrative arc: What → So What → What Next (classic executive efficiency arc)
- Acts I-III: Author-driven narrative (WHAT happened, SO WHAT is the impact)
- Act IV: Prescriptive recommendation (WHAT NEXT — fix the distribution)

Advanced Features:
1. What-If Parameterization (Act IV slider)
2. Context-Aware Filtering (event selector highlights all charts)
3. Narrative Scrollytelling (single-page vertical scroll with act transitions)
4. Rich Tooltips (Plotly hovertemplate on all charts)
"""
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="The Tariff Tax: Who Pays?",
    page_icon="⚖️",   # Scales of justice — ties to the "Who pays? Is it fair?" thesis
    layout="wide",
    initial_sidebar_state="expanded",
)

# Imports
from data_loader import (
    load_viz1, load_viz2, load_viz3, load_viz4,
    load_viz5, load_viz6, load_viz6_animated, load_viz6_consumer,
    load_viz7, load_viz8,
    load_key_events, load_commodity_prices, load_customs_duties,
)
from components import hook, act1_scale, act2_who_pays, act3_tradeoffs, act4_choice
from config import COLORS
from styles import (
    GLOBAL_CSS, act_banner, transition_text, visual_anchor, event_card,
    act_intro, ASSETS_DIR,
)

# Inject global CSS
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# --- Sidebar: editorial contents panel (brand head + ToC + event filter + credits) ---
with st.sidebar:
    # Masthead — brand + tagline. Matches the Playfair/Inter typography locked
    # in the main content, so the sidebar reads as part of the publication,
    # not as a separate control panel.
    st.markdown("""
    <div class="sb-head">
        <div class="sb-eyebrow">For the 47th President of the United States</div>
        <div class="sb-brand">The Tariff Tax</div>
        <div class="sb-tag">Who actually paid?</div>
    </div>
    """, unsafe_allow_html=True)

    # Editorial table of contents. Four acts + opening. Each row is a link
    # with a Roman numeral, an Act title, and the guiding question. Hover
    # reveals a gold left-border and slight nudge — tactile without motion
    # for motion's sake.
    st.markdown("""
    <div class="sb-label">Contents</div>
    <nav class="sb-nav">
      <a href="#the-tariff-tax-who-pays" class="sb-opening">
        <span class="sb-roman">OPEN</span>
        <span><span class="sb-title">The Opening</span><br>
              <span class="sb-question">$364B. Who pays?</span></span>
      </a>
      <a href="#act-i">
        <span class="sb-roman">I</span>
        <span><span class="sb-title">The Scale</span><br>
              <span class="sb-question">How big is this policy change?</span></span>
      </a>
      <a href="#act-ii">
        <span class="sb-roman">II</span>
        <span><span class="sb-title">Who Pays</span><br>
              <span class="sb-question">Is the burden fair?</span></span>
      </a>
      <a href="#act-iii">
        <span class="sb-roman">III</span>
        <span><span class="sb-title">What Did It Buy</span><br>
              <span class="sb-question">Did the promises land?</span></span>
      </a>
      <a href="#act-iv">
        <span class="sb-roman">IV</span>
        <span><span class="sb-title">The Choice</span><br>
              <span class="sb-question">98 days to decide.</span></span>
      </a>
    </nav>
    """, unsafe_allow_html=True)

    # Context-Aware Filtering (advanced feature). Selecting an event:
    #   (1) highlights a window around its date on every time-series chart
    #   (2) filters time-series charts to that window
    #   (3) filters Act II price-impact chart to affected_categories
    #   (4) shows a narrative card (title, detail, real photo, source link)
    st.markdown('<div class="sb-label">Event Filter</div>', unsafe_allow_html=True)
    key_events = load_key_events()
    event_options = ["None"] + [
        f"{row['date'].strftime('%Y-%m-%d')}: {row['event_short']}"
        for _, row in key_events.iterrows()
    ]
    selected = st.selectbox("Highlight an event:", event_options, key="event_filter",
                            label_visibility="collapsed")

    selected_event = None        # pandas.Timestamp or None — date of selected event
    selected_event_row = None    # pandas.Series or None — full row for richer wiring
    if selected != "None":
        date_str = selected.split(":")[0].strip()
        selected_event = pd.to_datetime(date_str)
        evt_row = key_events[key_events["date"] == selected_event].iloc[0]
        selected_event_row = evt_row
        st.markdown(event_card(
            event_short=evt_row["event_short"],
            event_detail=evt_row["event_detail"],
            event_date=evt_row["date"].strftime("%B %d, %Y"),
            tariff_rate=float(evt_row["eff_tariff_rate_approx"]),
            image_path=str(evt_row.get("image_path", "") or ""),
            source_url=str(evt_row.get("source_url", "") or ""),
            assets_root=ASSETS_DIR,
        ), unsafe_allow_html=True)

    # Footer — data colophon only, styled as a newspaper masthead line.
    # Academic provenance lives in README / docs, not in the user-facing UI.
    st.markdown("""
    <div class="sb-foot">
        <div class="sb-foot-row">
            <strong>Sources</strong><span class="sb-dot"></span>Federal Reserve<span class="sb-dot"></span>Yale Budget Lab<span class="sb-dot"></span>BLS<span class="sb-dot"></span>Tax Policy Center<span class="sb-dot"></span>Global Trade Alert<span class="sb-dot"></span>DFAT
        </div>
        <div class="sb-foot-row">
            Prepared from public data through <strong>April 2026</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Load all data ---
viz1 = load_viz1()
viz2 = load_viz2()
viz3 = load_viz3()
viz4 = load_viz4()
viz5 = load_viz5()
viz6 = load_viz6()
viz6_anim = load_viz6_animated()
viz6_consumer = load_viz6_consumer()
viz7 = load_viz7()
viz8 = load_viz8()
commodity_prices = load_commodity_prices()
customs = load_customs_duties()

# =============================================================
# HOOK — The opening (full-bleed visual anchor + narrative hook)
# =============================================================
st.markdown(visual_anchor(
    title="$364 BILLION",
    subtitle="A tax in everything but name.",
    eyebrow="The Tariff Tax — A Briefing for the President",
    image_path="images/hook_hero.jpg",
    icon="shopping-cart",
    large=True,
    attribution="Kees Torn / Wikimedia Commons, CC BY-SA 2.0",
    assets_root=ASSETS_DIR,
), unsafe_allow_html=True)
hook.render()

# =============================================================
# ACT I — THE SCALE
# =============================================================
st.markdown('<div id="act-i"></div>', unsafe_allow_html=True)
st.markdown(act_banner("I", "THE SCALE", "How big is this policy change?"), unsafe_allow_html=True)
act1_scale.render(viz1, key_events, viz6_anim, selected_event, selected_event_row)
st.markdown(transition_text('"Markets recover. People don\'t."'), unsafe_allow_html=True)

# =============================================================
# ACT II — WHO PAYS
# =============================================================
st.markdown('<div id="act-ii"></div>', unsafe_allow_html=True)
st.markdown(act_banner("II", "WHO PAYS", "Who bears the cost? Is it fair?"), unsafe_allow_html=True)
act2_who_pays.render(viz3, viz2, commodity_prices, selected_event, selected_event_row)
st.markdown(transition_text(
    '"$400 to a family earning $25,000 is rent.<br>'
    '$40,000 to a family earning $5 million is a rounding error.<br>'
    'Same policy. Vastly different pain. So what did it buy?"'
), unsafe_allow_html=True)

# =============================================================
# ACT III — WHAT DID IT BUY
# =============================================================
st.markdown('<div id="act-iii"></div>', unsafe_allow_html=True)
st.markdown(act_banner("III", "WHAT DID IT BUY", "What were the trade-offs?"), unsafe_allow_html=True)
act3_tradeoffs.render(viz4, viz5, viz6_consumer, customs, selected_event, selected_event_row)
st.markdown(transition_text(
    '"The tariffs bought leverage. The window to use it is closing."'
), unsafe_allow_html=True)

# =============================================================
# ACT IV — THE CHOICE
# =============================================================
st.markdown('<div id="act-iv"></div>', unsafe_allow_html=True)
st.markdown(act_banner("IV", "THE CHOICE", "What happens next?"), unsafe_allow_html=True)
act4_choice.render(viz7, viz8, viz3, customs, selected_event, selected_event_row)

# =============================================================
# FOOTER — in-character colophon, no rubric language.
# Academic provenance (course, advanced-features claim, etc.) lives in
# README.md and docs/persona.md, not in the user-facing briefing.
# =============================================================
st.divider()
st.markdown("""
<div style="text-align: center; padding: 1.2rem 1rem 0.5rem 1rem; color: #7F8C8D;
            font-family: 'Inter', sans-serif; font-size: 0.8rem; line-height: 1.7;">
    <span style="color:#F5B041; letter-spacing:2px; font-size:0.65rem;">
        DATA · APRIL 2026
    </span><br>
    Federal Reserve &middot; Yale Budget Lab &middot; Tax Policy Center &middot; Bureau of Labor Statistics &middot;
    Bureau of Economic Analysis &middot; Global Trade Alert &middot; US Census &middot; DFAT Australia<br>
    <span style="font-family: 'Playfair Display', Georgia, serif; font-style: italic; font-size: 0.85rem; color:#C0C0C0;">
        The tariff generated $364B in one year. The question is not whether to keep it — but who should keep paying for it.
    </span>
</div>
""", unsafe_allow_html=True)
