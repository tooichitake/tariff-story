"""Act I: THE SCALE — How big is this policy change?
Viz 1: Tariff rate staircase (step function with event annotations)
Viz 2: Market panic (S&P 500 + VIX dual-axis with event bands)
Viz 3: Animated global tariff map (choropleth over time)
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from config import COLORS, IMPACT_COLORS, CHART_LAYOUT, show_chart
from styles import chart_header, styled_metric_card, highlight_event_window


def render(viz1, key_events, viz6_anim, selected_event, selected_event_row=None):
    """Render Act I — THE SCALE. Narrative beat: awe / shock at speed and magnitude.

    Visuals:
      - Viz 1: Tariff-rate staircase (step function, event-annotated)
      - Viz 2: Market panic dual-axis (S&P 500 price + VIX fear index)
      - Viz 3: Animated global choropleth (effective tariff by country over time)

    Args:
        viz1: DataFrame — daily tariff rate + S&P 500 + VIX + event flags.
            Required cols: date, eff_tariff_rate, sp500, vix, event_short, is_event.
        key_events: DataFrame — event log. Required cols: date, event_short,
            event_detail, impact_type, eff_tariff_rate_approx, story_act.
        viz6_anim: DataFrame or None — country-level tariff snapshots for the
            animated choropleth. Required cols: date, iso3, country, effective_tariff.
        selected_event: pandas.Timestamp or None — if set, highlights the window
            around this date across charts and filters time-series to ±window_days.
        selected_event_row: pandas.Series or None — full row for the selected event,
            including ``window_days`` and ``image_path`` for richer filtering.

    Narrative intent:
        Open with "this moved faster and wider than most policy in a century."
        Peak-rate metric + 107-day climb + animated world map sell the scale.
    """
    # Resolve filter window (default 14 days if the event doesn't specify)
    _window = 14
    if selected_event_row is not None and pd.notna(selected_event_row.get("window_days")):
        try:
            _window = int(selected_event_row["window_days"])
        except (ValueError, TypeError):
            _window = 14
    # --- Key metrics ---
    peak = viz1["eff_tariff_rate"].max()
    col1, col2, col3 = st.columns(3)
    with col1:
        with styled_metric_card("#E74C3C"):
            st.metric("Peak Tariff Rate", f"{peak:.0f}%", "from 2.5%")
    with col2:
        with styled_metric_card(COLORS["gold"]):
            st.metric("Time to Peak", "107 days", "Jan 20 - Apr 10")
    with col3:
        with styled_metric_card("#3498DB"):
            st.metric("Countries Affected", "57+", "including allies")

    # --- Viz 1: Tariff Rate Staircase ---
    st.markdown(chart_header(
        "Century-High Tariffs in 107 Days",
        "Daily effective US import-weighted tariff rate, Jan 2025 - present"
    ), unsafe_allow_html=True)

    fig1 = go.Figure()

    # Main tariff-rate staircase. Gold (#F5B041) per the locked COLOR_SEMANTICS
    # rule in config.py: amber = accent / warning. Prior version used #FF8C00.
    fig1.add_trace(go.Scatter(
        x=viz1["date"], y=viz1["eff_tariff_rate"],
        mode="lines", line=dict(color=COLORS["gold"], width=3, shape="hv"),
        fill="tozeroy", fillcolor="rgba(245, 176, 65, 0.10)",
        name="Effective Tariff Rate",
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Tariff Rate: %{y:.1f}%<extra></extra>",
    ))

    # H6: Liberation Day accent marker — a single distinguished point on the
    # staircase, treated editorially (bigger, haloed) so the eye catches the
    # apex of the climb without needing to read any label. FT/NYT style.
    lib_day = pd.Timestamp("2025-04-02")
    lib_rate = viz1.loc[viz1["date"] == lib_day, "eff_tariff_rate"]
    if not lib_rate.empty:
        lib_y = float(lib_rate.iloc[0])
        # Halo
        fig1.add_trace(go.Scatter(
            x=[lib_day], y=[lib_y],
            mode="markers",
            marker=dict(size=22, color="rgba(231, 76, 60, 0.25)", line=dict(width=0)),
            showlegend=False, hoverinfo="skip",
        ))
        # Inner dot
        fig1.add_trace(go.Scatter(
            x=[lib_day], y=[lib_y],
            mode="markers",
            marker=dict(size=10, color="#E74C3C",
                        line=dict(color="#FAFAFA", width=2)),
            showlegend=False,
            hovertemplate="<b>Liberation Day — 2025-04-02</b><br>Tariff Rate: %{y:.1f}%<br>"
                          "<i>Sweeping reciprocal tariffs announced</i><extra></extra>",
        ))

    # --- Event annotation design (Phase 2 simplified) ---
    # Earlier iterations pinned 12 labels to this chart — the result was a
    # visual thicket that hid the climb. FT/NYT-style editorial restraint:
    # three lead annotations carry the arc (start, apex, current); the rest
    # remain as faint tick marks that reveal full detail only on hover.
    BADGE_BG = "rgba(20, 24, 32, 0.92)"
    TEXT_COLOR = "#FAFAFA"

    LEAD_LABELS = {
        "Trump inaugurated":       dict(ax=-70, ay=-30, headline="Jan 20 · 2.5%"),
        "Liberation Day":          dict(ax=0,   ay=-55, headline="Apr 2 · 22%<br>Sweeping reciprocal tariffs"),
        "Section 122 takes effect": dict(ax=-20, ay=-50, headline="Feb 24 · 13%<br>Post-SCOTUS replacement"),
    }

    for _, evt in key_events.iterrows():
        name = evt["event_short"]
        is_lead = name in LEAD_LABELS

        # Every event still gets a faint tick — data honesty. Lead events get
        # a brighter tick so the three labels feel anchored in the line.
        tick_color = COLORS["gold"] if is_lead else "#444444"
        tick_opacity = 0.55 if is_lead else 0.22
        fig1.add_vline(
            x=evt["date"].timestamp() * 1000,
            line=dict(color=tick_color, width=0.8 if is_lead else 0.6, dash="dot"),
            opacity=tick_opacity,
        )

        if is_lead and pd.notna(evt.get("eff_tariff_rate_approx")):
            cfg = LEAD_LABELS[name]
            fig1.add_annotation(
                x=evt["date"], y=evt["eff_tariff_rate_approx"],
                text=f"<b>{name}</b><br><span style='font-size:9px;color:#C0C0C0'>{cfg['headline']}</span>",
                showarrow=True,
                arrowhead=2, arrowsize=0.7, arrowwidth=1.2, arrowcolor=COLORS["gold"],
                font=dict(size=11, color=TEXT_COLOR),
                bgcolor=BADGE_BG,
                bordercolor=COLORS["gold"], borderwidth=1, borderpad=5,
                ax=cfg["ax"], ay=cfg["ay"],
                align="left",
            )

    if selected_event is not None:
        highlight_event_window(fig1, selected_event, window_days=_window)

    # Event-aware x-axis: when an event is selected, zoom to ±window_days;
    # otherwise show the full narrative range.
    if selected_event is not None:
        delta = pd.Timedelta(days=_window)
        x_range = [selected_event - delta, selected_event + delta]
    else:
        x_range = ["2024-12-01", pd.Timestamp("today") + pd.Timedelta(days=14)]

    fig1.update_layout(
        **CHART_LAYOUT,
        yaxis_title="Effective Tariff Rate (%)",
        xaxis_title="",
        showlegend=False,
        xaxis=dict(
            range=x_range,
            gridcolor="rgba(80, 80, 80, 0.15)",
            tickfont=dict(color="#888888"),
        ),
        yaxis=dict(
            range=[0, max(peak * 1.15, 30)],
            gridcolor="rgba(80, 80, 80, 0.15)",
            tickfont=dict(color="#888888"),
            title_font=dict(color="#888888"),
        ),
    )
    show_chart(fig1, height=500)

    # --- Viz 2: Market Fear (VIX only) ---
    # Prior version stacked S&P 500 with VIX on dual axes. The S&P recovered —
    # the story is not "the market crashed" but "fear spiked on every
    # announcement," which is what VIX tracks. Single axis, single line, event
    # bands do the heavy lifting.
    st.markdown(chart_header(
        "Fear Spiked on Every Announcement",
        "CBOE Volatility Index (VIX) with tariff-up event bands, 2025 onwards"
    ), unsafe_allow_html=True)

    viz1_focus = viz1[viz1["date"] >= "2025-01-01"].copy()

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=viz1_focus["date"], y=viz1_focus["vix"],
        mode="lines", line=dict(color=COLORS["accent_red"], width=2.5),
        fill="tozeroy", fillcolor="rgba(231, 76, 60, 0.08)",
        name="VIX (Fear Index)", connectgaps=True,
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>VIX: %{y:.1f}<extra></extra>",
    ))

    # Amber bands on tariff-up days — lets the eye scan "each red spike
    # sits on a golden band" without reading labels.
    for _, evt in key_events.iterrows():
        if evt["impact_type"] == "tariff_up" and evt["date"] >= pd.Timestamp("2025-01-01"):
            fig2.add_vrect(
                x0=evt["date"] - pd.Timedelta(days=1),
                x1=evt["date"] + pd.Timedelta(days=1),
                fillcolor="rgba(245, 176, 65, 0.12)", line=dict(width=0),
            )

    if selected_event is not None and selected_event >= pd.Timestamp("2025-01-01"):
        highlight_event_window(fig2, selected_event, window_days=_window)

    fig2.update_layout(
        **CHART_LAYOUT,
        showlegend=False,
        yaxis_title="VIX",
    )
    if selected_event is not None and selected_event >= pd.Timestamp("2025-01-01"):
        delta = pd.Timedelta(days=_window)
        fig2.update_xaxes(range=[selected_event - delta, selected_event + delta])
    show_chart(fig2, height=380)

    # ==========================================================
    # Viz 3: Animated Global Tariff Map — the spread
    # ==========================================================
    if viz6_anim is not None and len(viz6_anim) > 0:
        st.markdown(chart_header(
            "107 Days. 57 Countries.",
            "Watch tariff rates spread across the globe — use the slider to step through time"
        ), unsafe_allow_html=True)

        fig3 = px.choropleth(
            viz6_anim,
            locations="iso3",
            color="effective_tariff",
            animation_frame="date_str",
            hover_name="country_name",
            color_continuous_scale=[COLORS["green"], COLORS["gold"], COLORS["accent_red"]],
            range_color=[0, 50],
            labels={"effective_tariff": "Tariff Rate (%)", "date_str": "Date"},
            hover_data={"effective_tariff": ":.1f", "iso3": False},
        )
        fig3.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 800
        fig3.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 400
        fig3.layout.updatemenus[0].buttons[0].args[1]["transition"]["easing"] = "cubic-in-out"

        fig3.update_layout(
            **CHART_LAYOUT,
            geo=dict(
                showframe=False, showcoastlines=True,
                projection_type="natural earth",
                coastlinecolor="rgba(127,140,141,0.3)",
                bgcolor="rgba(0,0,0,0)",
                landcolor="rgba(15,22,32,0.8)",
                showland=True,
            ),
            coloraxis_colorbar=dict(title="Tariff %", len=0.6),
        )
        show_chart(fig3, height=500)
