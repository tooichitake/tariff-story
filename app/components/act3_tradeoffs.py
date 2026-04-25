"""Act III: WHAT DID IT BUY — Promise vs Verdict.
Viz 6: Deficit paradox (bar + line dual-axis)
Viz 7: Manufacturing trade-off (connected scatter)
Viz 8: Global tariff map (animated choropleth + Australia callout)
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from config import COLORS, CHART_LAYOUT, show_chart
from styles import (
    chart_header, insight_box, styled_metric_card,
    highlight_event_window, scorecard, act_intro,
)


def render(viz4, viz5, viz6_consumer, customs, selected_event, selected_event_row=None):
    """Render Act III — WHAT DID IT BUY. Narrative beat: complexity / honest trade-offs.

    Visuals:
      - Revenue bar chart (quarterly customs duties, annualized)
      - Promise 1 (deficit paradox): trade balance + tariff rate dual-axis
      - Promise 2 (factories): manufacturing employment change + job openings dual-axis
      - Promise 3 ("where your shoes come from"): country consumer-goods tariff map

    Args:
        viz4: DataFrame — monthly trade balance + tariff rate. Required cols:
            date, trade_balance, eff_tariff_rate.
        viz5: DataFrame — monthly mfg indicators + tariff rate. Required cols:
            date, mfg_employment, mfg_job_openings, eff_tariff_rate.
            Manufacturing baseline anchored on Jan 2025 (Trump inauguration) to
            align with BLS "since Jan 2025" framing in key_events.csv.
        viz6_consumer: DataFrame or None — country-level consumer-goods weighted
            tariff increase. Cols: iso3, country, weighted_tariff_increase_pct,
            top_category_1/2/3.
        customs: DataFrame or None — quarterly customs duties (annualized $B).
            Cols: date, customs_duties_bn.
        selected_event: pandas.Timestamp or None — when set, time-series charts
            zoom and highlight a window around this date.
        selected_event_row: pandas.Series or None — includes ``window_days``
            and ``affected_categories`` for richer filtering.

    Narrative intent:
        Pair every gain with its cost. Revenue up 4.4x → jobs down ~80K since
        Jan 2025. Deficit narrowed → but via import collapse, not export growth.
        Refuses a one-sided framing. This is the honesty load of the argument.
    """
    # Resolve per-event filter window (default 30 days for Act III monthly series)
    _window = 30
    if selected_event_row is not None and pd.notna(selected_event_row.get("window_days")):
        try:
            _window = int(selected_event_row["window_days"])
        except (ValueError, TypeError):
            _window = 30

    st.markdown(act_intro(
        "The tariffs were sold with four promises: more revenue, a smaller trade deficit, "
        "more manufacturing jobs, and greater leverage over trading partners. Some landed. "
        "Others didn't. The honest answer is not one-sided — and the President's briefing "
        "cannot afford to be either."
    ), unsafe_allow_html=True)

    # Compute the numbers that power the scorecard so they stay consistent
    # with the charts below (single source of truth).
    if customs is not None and len(customs) > 0:
        latest_rev = customs.iloc[-1]["customs_duties_bn"]
        baseline_rev = customs.iloc[0]["customs_duties_bn"]
        rev_multiplier = latest_rev / baseline_rev if baseline_rev > 0 else 0
        rev_actual = f"${latest_rev:.0f}B/yr ({rev_multiplier:.1f}x pre-tariff)"
    else:
        rev_actual = "$364B/yr (~4.4x pre-tariff)"

    # Manufacturing jobs delta anchored on Jan 2025 (Trump inauguration) —
    # aligns with the BLS "since Jan 2025" narrative framing used elsewhere.
    if "mfg_employment" in viz5.columns and viz5["mfg_employment"].notna().sum() > 1:
        mfg_series = viz5.dropna(subset=["mfg_employment"])
        baseline_rows = mfg_series[mfg_series["date"] >= "2025-01-01"]
        if len(baseline_rows) > 1:
            mfg_delta = int(baseline_rows["mfg_employment"].iloc[-1]
                            - baseline_rows["mfg_employment"].iloc[0])
            mfg_actual = f"{mfg_delta:+,d}K jobs since Jan 2025"
        else:
            mfg_delta = int(mfg_series["mfg_employment"].iloc[-1]
                            - mfg_series["mfg_employment"].iloc[0])
            mfg_actual = f"{mfg_delta:+,d}K jobs since Jan 2024"
    else:
        mfg_actual = "~-80K jobs since Jan 2025 (BLS)"

    # --- Promise vs Reality scorecard (the lead visual of Act III) ---
    st.markdown(chart_header(
        "Promise vs. Reality",
        "Four promises the tariffs were sold with. One was kept cleanly."
    ), unsafe_allow_html=True)
    st.markdown(scorecard([
        {
            "icon": "scale",
            "promise": "Generate significant new federal revenue",
            "actual": rev_actual,
            "verdict": "kept",
            "verdict_text": "Kept",
        },
        {
            "icon": "columns",
            "promise": "Shrink the US trade deficit",
            "actual": "Deficit narrowed, but via import collapse, not export growth",
            "verdict": "mixed",
            "verdict_text": "Mixed",
        },
        {
            "icon": "cog",
            "promise": "Bring manufacturing jobs home",
            "actual": mfg_actual,
            "verdict": "broken",
            "verdict_text": "Broken",
        },
        {
            "icon": "hand-coins",
            "promise": "Use tariffs as leverage at the negotiating table",
            "actual": "Geneva + Busan deals; allies also seeking alternatives",
            "verdict": "mixed",
            "verdict_text": "Mixed",
        },
    ]), unsafe_allow_html=True)

    # ==========================================================
    # PROMISE KEPT — Revenue (the one promise cleanly delivered)
    # ==========================================================
    if customs is not None and len(customs) > 0:
        st.markdown(chart_header(
            "Tariffs Raised $364B — a Four-Fold Jump",
            "Quarterly customs duties, annualized — the one promise that landed cleanly"
        ), unsafe_allow_html=True)

        baseline = customs.iloc[0]["customs_duties_bn"]
        latest = customs.iloc[-1]["customs_duties_bn"]
        multiplier = latest / baseline if baseline > 0 else 0

        fig_rev = go.Figure()
        bar_colors = [
            "#2ECC71" if v > baseline * 2 else COLORS["accent_blue"]
            for v in customs["customs_duties_bn"]
        ]
        fig_rev.add_trace(go.Bar(
            x=customs["date"], y=customs["customs_duties_bn"],
            marker=dict(color=bar_colors),
            text=[f"${v:.0f}B" for v in customs["customs_duties_bn"]],
            textposition="outside",
            hovertemplate="<b>%{x|%b %Y}</b><br>Revenue: $%{y:.1f}B/yr<extra></extra>",
        ))
        fig_rev.add_hline(
            y=baseline, line=dict(color=COLORS["muted"], dash="dash", width=1),
            annotation_text=f"Pre-tariff: ${baseline:.0f}B",
            annotation_font=dict(size=10, color=COLORS["muted"]),
        )
        fig_rev.update_layout(**CHART_LAYOUT, showlegend=False)
        fig_rev.update_yaxes(title_text="Customs Duties ($B, annualized)")
        show_chart(fig_rev, height=350)

    # ==========================================================
    # PROMISE BROKEN — Manufacturing jobs (before / after, one axis)
    # ==========================================================
    # Prior version used a dual-axis time series that forced the reader to
    # parse two lines on two scales. The honest story — "factories announced,
    # jobs disappeared" — is binary: employment then vs. now. Two bars carry
    # that story; unfilled-openings context goes underneath as a stat.
    has_mfg = "mfg_employment" in viz5.columns and viz5["mfg_employment"].notna().sum() > 1
    has_openings = "mfg_job_openings" in viz5.columns and viz5["mfg_job_openings"].notna().sum() > 1

    if has_mfg:
        mfg_series = viz5.dropna(subset=["mfg_employment"]).copy()
        trump_era = mfg_series[mfg_series["date"] >= "2025-01-01"]
        if len(trump_era) > 1:
            baseline_emp = float(trump_era["mfg_employment"].iloc[0])
            latest_emp = float(trump_era["mfg_employment"].iloc[-1])
            baseline_label = trump_era["date"].iloc[0].strftime("%b %Y")
            latest_label = trump_era["date"].iloc[-1].strftime("%b %Y")
        else:
            baseline_emp = float(mfg_series["mfg_employment"].iloc[0])
            latest_emp = float(mfg_series["mfg_employment"].iloc[-1])
            baseline_label = mfg_series["date"].iloc[0].strftime("%b %Y")
            latest_label = mfg_series["date"].iloc[-1].strftime("%b %Y")
        mfg_change = int(latest_emp - baseline_emp)
        mfg_change_str = f"{mfg_change:+,d}K"

        st.markdown(chart_header(
            "Factories Announced. Jobs Disappeared.",
            f"Manufacturing employment — {baseline_label} baseline vs. {latest_label} actual"
        ), unsafe_allow_html=True)

        fig_mfg = go.Figure(go.Bar(
            x=[f"{baseline_label} (baseline)", f"{latest_label} (now)"],
            y=[baseline_emp, latest_emp],
            marker=dict(color=[COLORS["accent_blue"], COLORS["accent_red"]]),
            text=[f"{baseline_emp:,.0f}K", f"{latest_emp:,.0f}K"],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Employment: %{y:,.0f}K<extra></extra>",
        ))
        # Annotation pinned to the "now" bar so the delta is unmissable.
        fig_mfg.add_annotation(
            x=1, y=latest_emp,
            text=f"<b>{mfg_change_str}</b> jobs",
            showarrow=False,
            font=dict(size=13, color=COLORS["accent_red"]),
            xanchor="center", yanchor="bottom", yshift=30,
        )
        # Y-axis starts near the data to make the drop visible — honest
        # framing since the caption names both absolute values.
        y_min = min(baseline_emp, latest_emp) - 300
        y_max = max(baseline_emp, latest_emp) + 200
        fig_mfg.update_layout(
            **CHART_LAYOUT,
            showlegend=False,
            yaxis=dict(range=[y_min, y_max], title_text="Employment (thousands)"),
        )
        show_chart(fig_mfg, height=380)

        openings_line = ""
        if has_openings:
            latest_openings = int(viz5["mfg_job_openings"].dropna().iloc[-1])
            openings_line = (
                f" Meanwhile, <b>{latest_openings:,d}K manufacturing positions</b> "
                f"remain unfilled — a skills gap that tariffs alone cannot close."
            )
        st.markdown(insight_box(
            f"Since Jan 2025, manufacturing employment has fallen by "
            f"<b>{abs(mfg_change):,d}K</b> — even as industrial production rose and "
            f"investment commitments surged.{openings_line}"
        ), unsafe_allow_html=True)

    # ==========================================================
    # DRILL-DOWN: secondary evidence tucked behind expanders so the
    # scorecard + two primary charts carry the narrative by default.
    # ==========================================================
    with st.expander("More context · The deficit paradox"):
        st.markdown(chart_header(
            "The Deficit Shrank — But at What Cost?",
            "Monthly US trade balance ($B). Imports collapsed before exports could grow."
        ), unsafe_allow_html=True)
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(
            x=viz4["date"], y=viz4["trade_balance"],
            name="Trade Balance ($B)",
            marker=dict(color=COLORS["accent_blue"], opacity=0.7),
            hovertemplate="<b>%{x|%b %Y}</b><br>Balance: $%{y:,.1f}B<extra></extra>",
        ))
        avg_2024 = viz4[viz4["date"] < "2025-01-01"]["trade_balance"].mean()
        if not pd.isna(avg_2024):
            fig6.add_hline(
                y=avg_2024, line=dict(color=COLORS["muted"], dash="dash", width=1),
                annotation_text=f"2024 avg: ${avg_2024:,.0f}B",
                annotation_font=dict(size=10, color=COLORS["muted"]),
            )
        if selected_event is not None:
            highlight_event_window(fig6, selected_event, window_days=_window)
        fig6.update_layout(**CHART_LAYOUT, showlegend=False)
        fig6.update_yaxes(title_text="Trade Balance ($B)")
        if selected_event is not None:
            delta = pd.Timedelta(days=_window)
            fig6.update_xaxes(range=[selected_event - delta, selected_event + delta])
        show_chart(fig6, height=360)

    with st.expander("More context · Who supplies the goods hit hardest"):
        st.markdown(chart_header(
            "Who Supplies the Goods Hit Hardest",
            "Top 10 source countries for US consumer goods, by weighted tariff increase"
        ), unsafe_allow_html=True)
        if viz6_consumer is not None and len(viz6_consumer) > 0:
            top10 = viz6_consumer.sort_values(
                "weighted_tariff_increase", ascending=True
            ).tail(10)
            # Single red with opacity gradient — matches Act II category chart
            # so the visual language is consistent across the two acts.
            vmax = float(top10["weighted_tariff_increase"].max()) or 1.0
            bar_colors = [
                f"rgba(231, 76, 60, {0.35 + 0.60 * (v / vmax):.2f})"
                for v in top10["weighted_tariff_increase"]
            ]
            fig_goods = go.Figure(go.Bar(
                y=top10["country_name"],
                x=top10["weighted_tariff_increase"],
                orientation="h",
                marker=dict(color=bar_colors),
                text=[f"+{v:.0f}%" for v in top10["weighted_tariff_increase"]],
                textposition="outside",
                customdata=list(zip(
                    top10["top_goods_affected"],
                    top10["total_consumer_imports_bn"],
                )),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Tariff increase: +%{x:.1f}%<br>"
                    "Consumer imports: $%{customdata[1]:.1f}B<br>"
                    "Top goods: %{customdata[0]}<extra></extra>"
                ),
            ))
            fig_goods.update_layout(
                **CHART_LAYOUT,
                xaxis_title="Weighted Tariff Increase (%)",
                showlegend=False,
            )
            show_chart(fig_goods, height=420)
        st.markdown(insight_box(
            "China supplies <b>$119B</b> in electronics (+27%) and <b>$30B</b> in toys (+36%). "
            "Vietnam supplies <b>$47B</b> in electronics (+11%) and <b>$13B</b> in furniture (+20%). "
            "These are the goods low-income families buy the most — "
            "and they come from the countries taxed the hardest."
        ), unsafe_allow_html=True)
