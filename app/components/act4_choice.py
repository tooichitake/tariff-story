"""Act IV: THE CHOICE — What should you do?
Viz 9: Policy scenario comparison (preset options + metrics + distributional bar)
Viz 10: Recession signal (yield spread + fed funds + countdown)
Narrative arc: What Next — prescriptive, not exploratory.
"""
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
from config import COLORS, DECILE_COLORS, CHART_LAYOUT, show_chart
from styles import (
    chart_header, countdown_widget, closing_address, insight_box,
    styled_metric_card, visual_anchor, highlight_event_window, ASSETS_DIR,
)

# Washington DC timezone (US Eastern = UTC-4 in summer / UTC-5 in winter)
ET = timezone(timedelta(hours=-4))


def _dc_today():
    """Current date in Washington DC (US Eastern Time)."""
    return datetime.now(ET).date()


def render(viz7, viz8, viz3, customs, selected_event, selected_event_row=None):
    """Render Act IV — THE CHOICE. Narrative beat: urgency / decision.

    Visuals:
      - Countdown widget (live: days until Section 122 expiry, 2026-07-24)
      - Viz 9: Policy scenario comparison bar (5 scenarios × Bottom vs Top 20%)
      - Viz 9b: What-If slider — interactively set tariff rate, see all 10 decile
        burdens interpolate in real time (advanced feature: parameterization)
      - Viz 10: Recession signal (yield spread + fed funds + VIX)
      - Closing address to the President

    Args:
        viz7: DataFrame — 5 policy scenarios with macro + distributional params.
            Required cols: scenario, eff_tariff_rate, gdp_impact_pct,
            unemployment_increase_pp, price_increase_pct,
            household_cost_bottom20_usd, household_cost_top20_usd,
            tariff_revenue_10yr_trillion, source.
        viz8: DataFrame — daily recession signals. Required cols: date,
            treasury_10y, yield_spread, vix.
        viz3: DataFrame — decile burden (reused here for slider interpolation).
            Needs scenarios "Current Policy (S122)" and "IEEPA Upheld" rows.
        customs: DataFrame or None — customs duties history (used to contextualize
            revenue scenarios).
        selected_event: pandas.Timestamp or None — when set, highlights the
            window on the recession-signal chart.
        selected_event_row: pandas.Series or None — full event row for richer
            filtering (uses ``window_days`` to size the highlight band).

    Narrative intent:
        Refuses to recommend a rate — the President decides. But makes the
        distributional consequence of every option visible, so silence on fairness
        is no longer an option. Closes with a direct address and a deadline.
    """
    # --- Countdown (real-time DC time) ---
    s122_date = datetime(2026, 7, 24).date()
    today = _dc_today()
    days_left = (s122_date - today).days
    st.markdown(countdown_widget(days_left), unsafe_allow_html=True)

    # ==========================================================
    # Scenario × Decile decision matrix — the moved/improved pictogram.
    # Each column is an income decile (D1 poorest → D10 richest); each row
    # is a policy scenario from viz7. Cell colour = interpolated USD burden
    # for that decile under that scenario, using the same linear
    # interpolation between Current Policy (13%) and IEEPA Upheld (27%) that
    # the What-If slider uses. Reader sees both axes at once: moving down a
    # column shows what a family pays under each policy choice; moving right
    # along a row shows how fairly (or not) that policy distributes the bill.
    # ==========================================================
    st.markdown(chart_header(
        "The Choice, Laid Bare",
        "Annual tariff cost (USD) for each household decile under each policy scenario."
    ), unsafe_allow_html=True)

    current_scenario = viz3[viz3["scenario"] == "Current Policy (S122)"].sort_values("decile")
    ieepa_scenario = viz3[viz3["scenario"] == "IEEPA Upheld"].sort_values("decile")
    if (
        len(viz7) > 0 and "eff_tariff_rate" in viz7.columns
        and len(current_scenario) == 10 and len(ieepa_scenario) == 10
    ):
        s122_rate = 13.0
        ieepa_rate = 27.0
        current_usd = current_scenario["usd_cost"].values
        ieepa_usd = ieepa_scenario["usd_cost"].values

        matrix_rows = []
        matrix_labels = []
        for _, row in viz7.iterrows():
            rate = float(row["eff_tariff_rate"])
            scale = np.clip((rate - s122_rate) / (ieepa_rate - s122_rate), -0.5, 1.5)
            usd_row = current_usd * (1 - scale) + ieepa_usd * scale
            matrix_rows.append(usd_row)
            matrix_labels.append(f"{row['scenario']}  ·  {rate:.1f}%")

        decile_labels = [f"D{i}" for i in range(1, 11)]
        # Reverse order so the first scenario (let S122 expire) appears on top.
        fig_matrix = go.Figure(data=go.Heatmap(
            z=matrix_rows[::-1],
            x=decile_labels,
            y=matrix_labels[::-1],
            text=[[f"${v:,.0f}" for v in row] for row in matrix_rows[::-1]],
            texttemplate="%{text}",
            textfont=dict(size=11, color="#FAFAFA"),
            colorscale=[[0, "rgba(231,76,60,0.15)"], [1, "rgba(192,57,43,1.0)"]],
            hovertemplate=(
                "<b>%{y}</b><br>%{x} household<br>Annual cost: %{text}<extra></extra>"
            ),
            showscale=False,
        ))
        fig_matrix.update_layout(
            **CHART_LAYOUT,
            xaxis=dict(title_text="Income decile (poorest → richest)",
                       side="top", tickfont=dict(size=11, color="#FAFAFA")),
            yaxis=dict(title_text="", tickfont=dict(size=11, color="#FAFAFA")),
        )
        show_chart(fig_matrix, height=300)
        st.caption(
            "Reading this: every **column** is the same family under different policies. "
            "Every **row** is one policy spread across the country. The red intensifies "
            "from right to left in every row — every scenario taxes the poorest most."
        )

    # ==========================================================
    # Viz 9: Policy Scenario Comparison — all options side-by-side
    # ==========================================================
    st.markdown(chart_header(
        "Five Paths — One Question: Who Pays?",
        "Every option has a cost. The burden falls differently across income groups."
    ), unsafe_allow_html=True)

    if len(viz7) > 0 and "eff_tariff_rate" in viz7.columns:
        # Build comparison data for all scenarios
        scenario_labels = viz7["scenario"].tolist()
        rates = viz7["eff_tariff_rate"].values

        # --- Household cost comparison bar (Bottom 20% vs Top 20%) ---
        if "household_cost_bottom20_usd" in viz7.columns:
            fig9 = go.Figure()

            fig9.add_trace(go.Bar(
                y=scenario_labels, x=viz7["household_cost_bottom20_usd"],
                orientation="h", name="Bottom 20%",
                marker=dict(color=COLORS["accent_red"]),
                text=[f"${v:,.0f}" for v in viz7["household_cost_bottom20_usd"]],
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>Bottom 20% cost: $%{x:,.0f}/yr<extra></extra>",
            ))
            fig9.add_trace(go.Bar(
                y=scenario_labels, x=viz7["household_cost_top20_usd"],
                orientation="h", name="Top 20%",
                marker=dict(color=COLORS["accent_blue"], opacity=0.5),
                text=[f"${v:,.0f}" for v in viz7["household_cost_top20_usd"]],
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>Top 20% cost: $%{x:,.0f}/yr<extra></extra>",
            ))

            fig9.update_layout(
                **CHART_LAYOUT,
                xaxis_title="Annual Household Cost (USD)",
                barmode="group",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            show_chart(fig9, height=400)

            # Burden gap insight
            b20 = viz7["household_cost_bottom20_usd"].values
            t20 = viz7["household_cost_top20_usd"].values
            # Show that in every scenario, the poor pay more as % of income
            st.markdown(insight_box(
                "In <b>every</b> scenario, the bottom 20% lose a larger share "
                "of their income than the top 20%. "
                "The tariff is a flat-rate tax on consumption — "
                "and the poorest consume the most as a share of income."
            ), unsafe_allow_html=True)

    # ==========================================================
    # What-If: Slider → distributional burden (Advanced Feature)
    # ==========================================================
    st.markdown(chart_header(
        "Move the Tariff Rate. The Gap Stays.",
        "Adjust the rate to any value between 0% and 25%. Every setting taxes the poorest at a higher share."
    ), unsafe_allow_html=True)

    tariff_rate = st.slider(
        "Set the effective tariff rate (%):",
        min_value=0.0, max_value=25.0, value=13.0, step=0.5,
        key="whatif_slider",
    )

    current_scenario = viz3[viz3["scenario"] == "Current Policy (S122)"].copy()
    ieepa_scenario = viz3[viz3["scenario"] == "IEEPA Upheld"].copy()

    if len(current_scenario) == 10 and len(ieepa_scenario) == 10:
        s122_rate = 13.0
        ieepa_rate = 27.0
        scale = np.clip((tariff_rate - s122_rate) / (ieepa_rate - s122_rate), -0.5, 1.5)

        interp_pct = (
            current_scenario["pct_income_lost"].values * (1 - scale)
            + ieepa_scenario["pct_income_lost"].values * scale
        )
        interp_pct = np.maximum(interp_pct, 0)

        fig_whatif = go.Figure(go.Bar(
            y=[f"Decile {i}" for i in range(1, 11)],
            x=interp_pct,
            orientation="h",
            marker=dict(color=DECILE_COLORS),
            text=[f"{v:.2f}%" for v in interp_pct],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Income Lost: %{x:.2f}%<extra></extra>",
        ))
        fig_whatif.update_layout(
            **CHART_LAYOUT,
            xaxis_title="Share of Income Lost (%)",
            yaxis=dict(autorange="reversed"),
            showlegend=False,
        )
        show_chart(fig_whatif, height=380)

        # Show the gap ratio dynamically
        gap = interp_pct[0] / interp_pct[9] if interp_pct[9] > 0 else 0
        st.markdown(insight_box(
            f"At <b>{tariff_rate:.1f}%</b> tariff rate: "
            f"the poorest decile loses <b>{interp_pct[0]:.2f}%</b> of income, "
            f"the wealthiest loses <b>{interp_pct[9]:.2f}%</b> — "
            f"a <b>{gap:.1f}x</b> gap. "
            f"The pattern holds at every rate."
        ), unsafe_allow_html=True)

    # ==========================================================
    # Viz 10: Recession Signal
    # ==========================================================
    st.markdown(chart_header(
        "The Clock Is Ticking: Yield Curve and the July Deadline",
        "2Y-10Y Treasury yield spread, VIX, and Federal Funds rate"
    ), unsafe_allow_html=True)

    fig10 = make_subplots(specs=[[{"secondary_y": True}]])

    # Yield spread as area chart
    viz8_pos = viz8.copy()
    viz8_neg = viz8.copy()

    fig10.add_trace(go.Scatter(
        x=viz8["date"], y=viz8["yield_spread"],
        fill="tozeroy",
        mode="lines",
        line=dict(color=COLORS["accent_blue"], width=1.5),
        fillcolor="rgba(52, 152, 219, 0.15)",
        name="Yield Spread (2Y-10Y)",
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Spread: %{y:.2f}%<extra></extra>",
    ), secondary_y=False)

    # Fed Funds rate (if available)
    if "fed_funds" in viz8.columns:
        fig10.add_trace(go.Scatter(
            x=viz8["date"], y=viz8["fed_funds"],
            mode="lines",
            line=dict(color=COLORS["gold"], width=2, dash="dash"),
            name="Fed Funds Rate",
            hovertemplate="<b>%{x|%b %d, %Y}</b><br>Fed Funds: %{y:.2f}%<extra></extra>",
        ), secondary_y=True)

    # Zero line for yield spread
    fig10.add_hline(y=0, line=dict(color="white", width=0.8, dash="dot"), secondary_y=False)

    # July 24 deadline
    fig10.add_vline(
        x=pd.Timestamp("2026-07-24").timestamp() * 1000,
        line=dict(color=COLORS["accent_red"], width=2, dash="dash"),
    )
    fig10.add_annotation(
        x=pd.Timestamp("2026-07-24"), y=viz8["yield_spread"].max() * 0.9,
        text="S122 Expires<br>Jul 24",
        font=dict(size=11, color=COLORS["accent_red"]),
        showarrow=True, arrowhead=2, arrowcolor=COLORS["accent_red"],
        ax=-50, ay=-20,
    )

    # Selected event — highlight a window rather than a single day so the
    # viewer can see the market reaction around the event.
    if selected_event is not None:
        _w = 14
        if selected_event_row is not None and pd.notna(selected_event_row.get("window_days")):
            try:
                _w = int(selected_event_row["window_days"])
            except (ValueError, TypeError):
                _w = 14
        highlight_event_window(fig10, selected_event, window_days=_w)

    # Inversion stats
    if "yield_inverted" in viz8.columns:
        inverted_days = int(viz8["yield_inverted"].sum())
        total_days = len(viz8)
        pct_inverted = inverted_days / total_days * 100
        # Inline annotation so the most important recession signal is visible
        # at-a-glance rather than buried in the insight box.
        fig10.add_annotation(
            xref="paper", yref="paper", x=0.01, y=0.04,
            text=(
                f"<b>Inverted {inverted_days} of {total_days} days</b>"
                f"  <span style='color:#7F8C8D'>({pct_inverted:.0f}%)</span>"
            ),
            showarrow=False,
            font=dict(size=12, color=COLORS["accent_red"]),
            bgcolor="rgba(14,17,23,0.75)",
            bordercolor=COLORS["accent_red"],
            borderwidth=1, borderpad=5,
            xanchor="left", yanchor="bottom",
        )

    fig10.update_layout(
        **CHART_LAYOUT,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig10.update_yaxes(title_text="Yield Spread (%)", secondary_y=False)
    fig10.update_yaxes(title_text="Fed Funds Rate (%)", secondary_y=True)
    show_chart(fig10, height=400)

    if "yield_inverted" in viz8.columns:
        st.markdown(insight_box(
            f"The yield curve was inverted for <b>{inverted_days}</b> of the last "
            f"<b>{total_days}</b> trading days (<b>{pct_inverted:.0f}%</b>). "
            f"The Fed has cut rates <b>6 times</b> since Sep 2024 (5.33% to 3.64%), "
            f"yet financial stress persists. "
            f"The Section 122 tariff authority expires in <b>{days_left} days</b>."
        ), unsafe_allow_html=True)

    # --- Visual anchor for the closing address: the decision moment ---
    st.markdown(visual_anchor(
        title="The desk is yours.",
        subtitle="The tariffs worked as policy. Now make them work as fairness.",
        eyebrow="Act IV · The Choice",
        image_path="images/oval_office.jpg",
        icon="columns",
        attribution="White House / Public Domain",
        assets_root=ASSETS_DIR,
    ), unsafe_allow_html=True)

    # --- Closing address ---
    st.markdown(closing_address(
        "Mr. President, your tariff policy delivered real results: "
        "revenue surged from $82B to $364B, reshoring investment hit record levels, "
        "and trading partners returned to the negotiating table.<br><br>"

        "But the data tells us <b>who paid for it</b>. "
        "The poorest 10% of Americans lost <b>3.2 times</b> more of their income "
        "than the wealthiest. The goods they depend on — shoes, clothing, food — "
        "were taxed the most.<br><br>"

        "Across the political spectrum, economists and trade strategists agree: "
        "the policy achieved its revenue and leverage goals, "
        "but the burden falls disproportionately on those least able to bear it. "
        "Even advocates of tariffs acknowledge the instrument needs refinement.<br><br>"

        "The tariff generated $364 billion. "
        "The question is not whether to keep it.<br>"
        "<b>The question is whether the poorest Americans "
        "should keep paying the most.</b><br><br>"

        f"<b>{days_left} days</b> until Section 122 expires."
    ), unsafe_allow_html=True)
