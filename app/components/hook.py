"""Landing hook: one number, one question, maximum impact."""
import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta


def render(viz3):
    """Render the opening hook: one number, one question, one countdown.

    Narrative intent: in ≤ 5 seconds, communicate (a) this is about money leaving
    American households, (b) the central question ("Who pays?"), (c) the clock
    is ticking (Section 122 expiry countdown). The distributional anchors
    ($_ from a family earning $_) are computed live from ``viz3``'s Current
    Policy row, so the Hook stays in lockstep with Act II's dumbbell and
    metric cards — no separate TPC/Yale figures to drift apart.

    Args:
        viz3: DataFrame with the decile-level burden rows. Required cols:
            scenario, decile, usd_cost, pct_income_lost. Uses the
            "Current Policy (S122)" scenario, deciles 1 (poorest) and 10
            (richest), to derive the two rhetorical dollar anchors.
    """
    # Real-time Washington DC date. Use date-only subtraction so the
    # countdown stays in lockstep with the sidebar and Act IV widgets —
    # `datetime - datetime` truncates by one day whenever DC isn't at
    # midnight, silently producing three different numbers.
    from datetime import date as _date
    ET = timezone(timedelta(hours=-4))
    dc_now = datetime.now(ET)
    date_str = dc_now.strftime("%B %d, %Y")
    s122_days = (_date(2026, 7, 24) - dc_now.date()).days

    # Distributional anchors: bottom 10% vs top 10% under Current Policy.
    # Dollar burden straight from viz3, income back-calculated as
    # usd_cost ÷ (pct_income_lost / 100) — same derivation the Act II
    # dumbbell uses, so Hook and Act II read from one source of truth.
    _cur = viz3[viz3["scenario"] == "Current Policy (S122)"].sort_values("decile")
    _d1 = _cur[_cur["decile"] == 1].iloc[0]
    _d10 = _cur[_cur["decile"] == 10].iloc[0]
    _d1_cost_raw = abs(float(_d1["usd_cost"]))
    _d1_income_raw = _d1_cost_raw / (abs(float(_d1["pct_income_lost"])) / 100.0)
    _d10_cost_raw = abs(float(_d10["usd_cost"]))
    _d10_income_raw = _d10_cost_raw / (abs(float(_d10["pct_income_lost"])) / 100.0)
    # Round for display: burden to nearest $10 ($430, $1,810); income to
    # nearest $1k ($38,000, $500,000). Raw figures like $1,809.48 read as
    # false precision for a rhetorical anchor and hurt the cadence.
    _d1_cost = round(_d1_cost_raw, -1)
    _d10_cost = round(_d10_cost_raw, -1)
    _d1_income = round(_d1_income_raw, -3)
    _d10_income = round(_d10_income_raw, -3)

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
            <span style="color:#E74C3C; font-weight:700;">${_d1_cost:,.0f}</span>
            <span style="color:#7F8C8D;">from a family earning ${_d1_income:,.0f}.</span><br>
            <span style="color:#E74C3C; font-weight:700;">${_d10_cost:,.0f}</span>
            <span style="color:#7F8C8D;">from a family earning ${_d10_income:,.0f}.</span>
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
