"""Landing hook: one number, one question, maximum impact."""
import streamlit as st
from datetime import datetime, timezone, timedelta


def render():
    """Render the opening hook: one number, one question, one countdown.

    Narrative intent: in ≤ 5 seconds, communicate (a) this is about money leaving
    American households ($3,800/yr), (b) the central question ("Who pays?"),
    (c) the clock is ticking (Section 122 expiry countdown). No data-loading
    arguments — all content is narrative-constant except the live DC date and
    countdown, which compute from the current time.
    """
    # Real-time Washington DC date
    ET = timezone(timedelta(hours=-4))
    dc_now = datetime.now(ET)
    date_str = dc_now.strftime("%B %d, %Y")
    s122_days = (datetime(2026, 7, 24, tzinfo=ET) - dc_now).days

    # Narrative tension over abstraction: lead with distributional inequality,
    # not a single per-household average. The two dollar figures below are
    # rhetorical anchors — "$400" and "$40,000" come directly from the
    # Yale Budget Lab distributional analysis (bottom quintile vs top 1%).
    st.markdown(f"""
    <div class="hook-container">
        <div style="font-size:0.8rem; color:#7F8C8D; letter-spacing:2px; text-transform:uppercase; margin-bottom:1.5rem;">
            Washington, D.C. &mdash; {date_str} &mdash; Effective tariff rate: 11.0%
        </div>
        <div class="hook-amount">$364B</div>
        <div class="hook-subtitle">Your tariff policy raised this in one year &mdash; more than any year since 1943.</div>
        <div style="margin: 1.5rem auto 0.5rem auto; max-width: 620px; font-family: 'Playfair Display', Georgia, serif; font-size: 1.35rem; color: #FAFAFA; line-height: 1.55;">
            <span style="color:#F5B041; letter-spacing:1.5px; font-size:0.75rem; text-transform:uppercase; font-family:'Inter',sans-serif; font-weight:600;">
                Mr. President
            </span><br>
            But the bill didn't land evenly.<br>
            <span style="color:#E74C3C; font-weight:700;">$400</span>
            <span style="color:#7F8C8D;">from a family earning $25,000.</span><br>
            <span style="color:#E74C3C; font-weight:700;">$40,000</span>
            <span style="color:#7F8C8D;">from a family earning $5,000,000.</span>
        </div>
        <div class="hook-question">Who actually paid?</div>
        <div style="font-size:0.95rem; color:#E74C3C; margin-top:1rem;">
            Section 122 expires in <b>{s122_days} days</b>
        </div>
        <div style="text-align:center; margin-top:2rem; font-size:1.5rem; color:#F5B041; opacity: 0.6;">
            &#x25BC;
        </div>
        <div style="text-align:center; color:#7F8C8D; font-size:0.9rem; margin-top:0.3rem;">
            Scroll down to find out
        </div>
    </div>
    """, unsafe_allow_html=True)
