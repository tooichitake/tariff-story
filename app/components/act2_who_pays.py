"""Act II: WHO PAYS — The emotional core of the narrative.
Viz 3: 10-decile income burden (horizontal bar, scenario toggle)
Viz 4: Price impact by category (horizontal bar)
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from config import COLORS, DECILE_COLORS, DECILE_INCOME_LABELS, CHART_LAYOUT, show_chart

from data_loader import load_us_income_distribution
from styles import (
    chart_header, insight_box, styled_metric_card, visual_anchor, act_intro,
    category_icon_svg, ASSETS_DIR,
)


# Pyramid Y-axis cap. Census's terminal bracket is "$250k+", so the chart
# visible range is $0-$275k (8 bands × $25k + 1 $50k band + a $25k sliver
# for the $250k+ open band; see scripts/15_download_census_income.py).
_PYRAMID_Y_MAX = 275_000


def render(viz3, viz2, commodity_prices, selected_event, selected_event_row=None):
    """Render Act II — WHO PAYS. The emotional core: regressive distributional burden.

    Visuals:
      - Viz 3: 10-decile income burden (horizontal bar + scenario/view toggles)
      - Viz 4: Price impact by product category (horizontal bar)

    Args:
        viz3: DataFrame — decile-level burden. Required cols: decile, decile_label,
            scenario, pct_income_lost, usd_cost, most_affected_goods.
            Must include both "Current Policy (S122)" and "IEEPA Upheld" scenarios.
        viz2: DataFrame — monthly tariff × CPI × sentiment join (not rendered in
            this act; reserved for future cross-references).
        commodity_prices: DataFrame or None — category-level price increase data.
            Optional cols: category, price_increase_pct. Falls back to hardcoded
            estimates if missing or too thin.
        selected_event: pandas.Timestamp or None — passed through for symmetry
            with other acts; viz4 uses ``selected_event_row['affected_categories']``.
        selected_event_row: pandas.Series or None — when present with a non-empty
            ``affected_categories`` field, viz4 is filtered to show only those
            categories (Tier 2 context-aware filter extension).

    Narrative intent:
        Punch-line: "3.2x more for the poorest." Bottom decile loses 1.14%, top
        decile 0.36% (Yale Budget Lab Feb 2026). Explicitly addresses the Fed's
        "transitory" framing: even a one-time shift leaves a regressive bill.
    """
    # --- Visual anchor: ground the abstract percentages in a concrete
    # consumer moment before the decile bar delivers the punchline.
    st.markdown(visual_anchor(
        title="The bill has already been paid.",
        subtitle="The bottom 10% loses 1.14% of income. The top 10% loses 0.36%. Same country. Different tax.",
        eyebrow="Act II · The Emotional Core",
        image_path="images/act2_hands.jpg",
        icon="hand-coins",
        attribution="Wikimedia Commons / Public Domain",
        assets_root=ASSETS_DIR,
    ), unsafe_allow_html=True)

    st.markdown(act_intro(
        "Tariffs look like a cost on foreign goods. They land on American households. "
        "Because low-income families spend a larger share of their budget on clothing, "
        "shoes, and food — the very categories most exposed to import tariffs — the "
        "burden is not shared equally. Even if the Fed is right that this is a one-time "
        "price shift, the bill is still regressive."
    ), unsafe_allow_html=True)

    # Back-calculate implied incomes + shares from Yale's decile data. The
    # same numbers power both the income pyramid (indirectly, via context
    # only) and the dumbbell below.
    current = viz3[viz3["scenario"] == "Current Policy (S122)"].sort_values("decile")
    _burden_usd = current["usd_cost"].abs().astype(float).values
    _pct_income = current["pct_income_lost"].abs().astype(float).values
    _implied_income = _burden_usd / (_pct_income / 100.0)
    _income_share = (100.0 * _implied_income / _implied_income.sum()).tolist()
    _burden_share = (100.0 * _burden_usd / _burden_usd.sum()).tolist()

    _color_income = "#3498DB"
    _color_burden = "#E74C3C"
    _color_regressive_line = "#E74C3C"
    _color_progressive_line = "#7F8C8D"

    # ======================================================================
    # CHART 1: Income pyramid — scene-setter. Establishes that most
    # Americans live at the bottom of the income distribution BEFORE the
    # dumbbell below shows what each slice pays.
    # ======================================================================
    # Load income distribution from Census (refreshed via
    # scripts/15_download_census_income.py → data/cleaned/census_income_distribution.csv).
    # Graceful fallback: if the file is missing the pyramid panel simply
    # doesn't render; Act II's other visuals stay intact.
    income_dist = load_us_income_distribution()
    if income_dist is None:
        st.info("Census household income distribution CSV not found. "
                "Run `python scripts/15_download_census_income.py` to fetch it.")
    else:
        _bands = []
        for row in income_dist.itertuples(index=False):
            lo = int(row.lo)
            hi = int(row.hi) if pd.notna(row.hi) else _PYRAMID_Y_MAX
            span = hi - lo
            center = (lo + hi) / 2
            _bands.append(dict(
                label=row.label, lo=lo, hi=hi,
                center=center, span=span, share=float(row.share_pct),
            ))

        st.markdown(chart_header(
            "Where Americans live",
            "U.S. household income distribution. Source: Census Bureau, CPS ASEC "
            "2025 (HINC-06). Bands are $25k wide up to $200k, then $50k wide to "
            "$250k, with a single open band for $250k and above."
        ), unsafe_allow_html=True)

        # Narrative markers — derived live from the loaded table.
        _cum_under_100k = sum(b["share"] for b in _bands if b["hi"] <= 100_000)
        _peak_band = max(_bands, key=lambda b: b["share"])
        _top_band = next(b for b in _bands if b["lo"] >= 250_000)

        fig_pop = go.Figure()
        for b in _bands:
            _is_peak = b is _peak_band
            bar_color = "rgba(245, 176, 65, 0.75)" if _is_peak else "rgba(127,140,141,0.55)"
            bar_text = (
                [f'{b["share"]:.1f}%' if b["share"] < 10 else f'{b["share"]:.0f}%']
                if b["share"] >= 1 else [""]
            )
            fig_pop.add_trace(go.Bar(
                x=[b["share"]],
                y=[b["center"]],
                orientation="h",
                width=b["span"] * 0.92,
                marker=dict(color=bar_color, line=dict(color="#0E1117", width=1)),
                text=bar_text,
                textposition="outside",
                textfont=dict(size=10, color="#C0C0C0"),
                hovertemplate=f'<b>{b["label"]}</b><br>{b["share"]:.1f}% of U.S. households<extra></extra>',
                showlegend=False,
            ))

        fig_pop.add_hline(
            y=100_000,
            line=dict(color="#F5B041", width=1, dash="dot"),
            annotation_text=f"<b>{_cum_under_100k:.0f}%</b> of U.S. households earn less than $100k",
            annotation_position="top right",
            annotation_font=dict(size=11, color="#F5B041"),
        )

        fig_pop.add_annotation(
            x=_peak_band["share"], y=_peak_band["center"],
            text=f"<b>Peak · live at {_peak_band['label']}</b>",
            showarrow=False,
            xanchor="left", yanchor="middle",
            xshift=55,
            font=dict(size=11, color="#F5B041"),
        )

        fig_pop.add_annotation(
            x=_top_band["share"], y=_top_band["center"],
            text=f"<b>{_top_band['share']:.0f}% earn $250k or more</b>",
            showarrow=False,
            xanchor="left", yanchor="middle",
            xshift=45,
            font=dict(size=11, color="#C0C0C0"),
        )

        _pop_layout = {k: v for k, v in CHART_LAYOUT.items() if k != "margin"}
        fig_pop.update_layout(
            **_pop_layout,
            margin=dict(l=90, r=40, t=30, b=55),
            bargap=0,
        )
        fig_pop.update_xaxes(
            title_text="% of U.S. households",
            gridcolor="rgba(127,140,141,0.12)",
            range=[0, 22],
        )
        fig_pop.update_yaxes(
            range=[0, _PYRAMID_Y_MAX],
            tickvals=[0, 25_000, 50_000, 75_000, 100_000, 125_000, 150_000, 175_000, 200_000, 250_000],
            ticktext=["$0", "$25k", "$50k", "$75k", "$100k", "$125k", "$150k", "$175k", "$200k", "$250k"],
            title_text="Household income",
            gridcolor="rgba(127,140,141,0.1)",
        )
        show_chart(fig_pop, height=460)

    # ======================================================================
    # CHART 2: Who earns, who pays — dumbbell with categorical (equal-
    # spaced) Y axis so the middle deciles get readable separation between
    # their income and burden dots. The income pyramid above already
    # covers the "most Americans live at the bottom" story visually; this
    # chart can focus on the regressivity comparison without needing to
    # carry population density too.
    # ======================================================================
    st.markdown(chart_header(
        "Who earns, who pays",
        "Each row is 10% of U.S. households, anchored by typical income. "
        "Blue dot = their share of national income. Red dot = their share "
        "of the tariff bill. A red line means that slice pays more than "
        "they earn. Source: Yale Budget Lab distributional analysis "
        "(Feb 2026), based on GTAP v7 with Census, BLS and BEA microdata."
    ), unsafe_allow_html=True)

    y_labels = list(DECILE_INCOME_LABELS)
    y_labels[0] = f"{y_labels[0]}  ·  poorest 10%"
    y_labels[-1] = f"{y_labels[-1]}  ·  richest 10%"

    # Connecting segments, per decile, with per-row colour + width. Line
    # widths bumped from 5/3 → 7/4 so mid-decile gaps (often sub-1.5pp)
    # register at glance distance; the line is the regressivity evidence,
    # so it should read heavier than the dots it connects.
    _segments = []
    for i in range(10):
        overpay = _burden_share[i] > _income_share[i]
        _segments.append(dict(
            type="line",
            xref="x", yref="y",
            x0=_income_share[i], x1=_burden_share[i],
            y0=y_labels[i], y1=y_labels[i],
            line=dict(
                color=_color_regressive_line if overpay else _color_progressive_line,
                width=7 if overpay else 4,
            ),
            layer="below",
        ))

    fig_pyr = go.Figure()
    fig_pyr.add_trace(go.Scatter(
        x=_income_share, y=y_labels,
        mode="markers+text",
        name="Share of U.S. income",
        marker=dict(size=15, color=_color_income, line=dict(color="#0E1117", width=1.5)),
        text=[f"{s:.1f}%" for s in _income_share],
        textposition=[
            "middle left" if _burden_share[i] > _income_share[i] else "middle right"
            for i in range(10)
        ],
        textfont=dict(size=11, color=_color_income),
        customdata=[[inc / 1000.0, sh] for inc, sh in zip(_implied_income, _income_share)],
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Typical income: ~$%{customdata[0]:.0f}k<br>"
            "Share of U.S. income: %{customdata[1]:.1f}%<extra></extra>"
        ),
    ))
    fig_pyr.add_trace(go.Scatter(
        x=_burden_share, y=y_labels,
        mode="markers+text",
        name="Share of tariff burden",
        marker=dict(size=15, color=_color_burden, line=dict(color="#0E1117", width=1.5)),
        text=[f"{s:.1f}%" for s in _burden_share],
        textposition=[
            "middle right" if _burden_share[i] > _income_share[i] else "middle left"
            for i in range(10)
        ],
        textfont=dict(size=11, color=_color_burden),
        customdata=[[u, sh] for u, sh in zip(_burden_usd, _burden_share)],
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Annual tariff cost: $%{customdata[0]:,.0f}<br>"
            "Share of tariff burden: %{customdata[1]:.1f}%<extra></extra>"
        ),
    ))

    _max_share = max(max(_income_share), max(_burden_share))
    _x_range = 1.12 * _max_share
    _pyr_layout = {k: v for k, v in CHART_LAYOUT.items() if k != "margin"}
    fig_pyr.update_layout(
        **_pyr_layout,
        margin=dict(l=150, r=60, t=20, b=55),
        shapes=_segments,
        xaxis=dict(
            tickvals=[0, 5, 10, 15, 20, 25, 30, 35],
            ticktext=["0", "5%", "10%", "15%", "20%", "25%", "30%", "35%"],
            title="Share of U.S. total",
            zeroline=True, zerolinecolor="#7F8C8D", zerolinewidth=1,
            range=[-1, _x_range],
            gridcolor="rgba(127,140,141,0.12)",
        ),
        yaxis=dict(
            categoryorder="array",
            categoryarray=y_labels,
            title="Typical household income",
            gridcolor="rgba(127,140,141,0.08)",
        ),
        showlegend=True,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1, bgcolor="rgba(0,0,0,0)",
        ),
    )
    show_chart(fig_pyr, height=500)

    # Short, declarative, matches the insight-box voice elsewhere in the
    # app (see act3 manufacturing insight, act4 yield-curve insight).
    st.markdown(insight_box(
        f"The richest 10% earns <b>{_income_share[9]:.0f}%</b> of U.S. income "
        f"and pays <b>{_burden_share[9]:.0f}%</b> of the tariff bill. "
        f"The poorest 10% earns <b>{_income_share[0]:.1f}%</b> and pays "
        f"<b>{_burden_share[0]:.1f}%</b>. "
        f"The bill lands hardest where most of America lives: below <b>$75k</b>."
    ), unsafe_allow_html=True)

    # --- Key metrics from decile data ---
    current = viz3[viz3["scenario"] == "Current Policy (S122)"]
    d1_pct = current.iloc[0]["pct_income_lost"]
    d10_pct = current.iloc[9]["pct_income_lost"]
    avg_cost = current["usd_cost"].mean()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with styled_metric_card("#E74C3C"):
            st.metric("Bottom 10%", f"-{d1_pct:.2f}%", "of income", delta_color="inverse")
    with col2:
        with styled_metric_card("#2ECC71"):
            st.metric("Top 10%", f"-{d10_pct:.2f}%", "of income", delta_color="inverse")
    with col3:
        with styled_metric_card(COLORS["gold"]):
            st.metric("Burden Gap", f"{d1_pct / d10_pct:.1f}x", "more for the poorest")
    with col4:
        with styled_metric_card("#3498DB"):
            st.metric("Avg Household", f"${avg_cost:,.0f}/yr", "annual cost")

    # --- Viz 3: per-household drill-down (scenario + view toggles, goods hover).
    # The macro share story is already told by the butterfly pyramid above;
    # this chart is the micro complement — what a specific household in each
    # slice pays under each policy, and which goods hurt most for them.
    st.markdown(chart_header(
        "What each household actually pays",
        "Switch scenarios to compare policies; switch views for % of income "
        "or raw dollars. Hover a bar to see the goods that drive that slice's "
        "bill. Source: Yale Budget Lab distributional analysis (Feb 2026)."
    ), unsafe_allow_html=True)

    # Scenario toggle
    scenario_col, view_col = st.columns([2, 1])
    with scenario_col:
        scenario = st.radio(
            "Policy scenario:",
            ["Current Policy (S122)", "IEEPA Upheld"],
            horizontal=True, key="scenario_toggle",
        )
    with view_col:
        view = st.radio("View:", ["% of Income", "USD Cost"], horizontal=True, key="view_toggle")

    data = viz3[viz3["scenario"] == scenario].sort_values("decile")
    y_col = "pct_income_lost" if view == "% of Income" else "usd_cost"
    x_label = "Share of Income Lost (%)" if view == "% of Income" else "Annual Cost (USD)"

    # Reader-facing y labels: typical household income per decile, not D1/D10
    # (data-science jargon that the President reader shouldn't have to decode).
    viz3_y_labels = [DECILE_INCOME_LABELS[int(d) - 1] for d in data["decile"]]

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        y=viz3_y_labels,
        x=data[y_col],
        orientation="h",
        marker=dict(color=DECILE_COLORS),
        text=[f"{v:.2f}%" if view == "% of Income" else f"${v:,.0f}" for v in data[y_col]],
        textposition="outside",
        hovertemplate=(
            "<b>Household earning %{y}</b><br>"
            + ("Income Lost: %{x:.2f}%" if view == "% of Income" else "Cost: $%{x:,.0f}")
            + "<br>Goods: %{customdata}<extra></extra>"
        ),
        customdata=data["most_affected_goods"],
    ))

    fig3.update_layout(
        **CHART_LAYOUT,
        xaxis_title=x_label,
        yaxis=dict(autorange="reversed", title="Typical household income"),
        showlegend=False,
    )
    show_chart(fig3, height=450)

    # The 100-person pictogram previously lived here. It was moved to Act IV
    # (re-purposed as a Scenario × Decile decision matrix) so that (a) Act II
    # is no longer telling the same story twice and (b) Act IV gains a
    # decision-grade visual that links policy choice to distributional impact.

    # --- Viz 4: Price Impact by Category ---
    # If an event is selected and it declares affected_categories, filter viz4
    # to only those categories — one of the advanced Context-Aware Filtering
    # behaviours. When the category list is empty or the event is unselected,
    # show all 10 categories.
    affected_set = set()
    if selected_event_row is not None:
        raw = selected_event_row.get("affected_categories", "")
        if isinstance(raw, str) and raw.strip():
            affected_set = {c.strip() for c in raw.split(",") if c.strip()}

    subtitle = "Estimated price increase by product category — the goods the poorest buy most"
    if affected_set:
        subtitle = (
            f"Filtered to categories directly affected by "
            f"<em>{selected_event_row['event_short']}</em>"
        )
    st.markdown(chart_header("Essentials Hit Hardest", subtitle), unsafe_allow_html=True)

    # Use commodity prices or fallback
    if commodity_prices is not None and len(commodity_prices) > 2:
        categories = commodity_prices
    else:
        categories = pd.DataFrame({
            "category": ["Footwear", "Apparel", "Toys & Games", "Household Textiles",
                         "Consumer Electronics", "Furniture", "Auto Parts", "Fresh Food",
                         "Machinery", "Pharmaceuticals"],
            "price_increase_pct": [39, 37, 28, 25, 18, 15, 12, 8, 6, 3],
        })

    cat_col = "category" if "category" in categories.columns else categories.columns[0]
    val_col = "price_increase_pct" if "price_increase_pct" in categories.columns else categories.columns[1]
    cat_df = categories.sort_values(val_col, ascending=True).head(10)

    # Apply event-driven filter when applicable.
    if affected_set:
        cat_df = cat_df[cat_df[cat_col].isin(affected_set)]
        if cat_df.empty:
            # The event's categories may not match any of our viz4 categories
            # exactly (e.g. "Pharmaceuticals" event, but the price list top-10
            # doesn't include Pharma). Fall back to showing all so the section
            # still renders.
            cat_df = categories.sort_values(val_col, ascending=True).head(10)

    # Single semantic colour (red = cost) with opacity encoding intensity.
    # Replaces a 4-hue step gradient (#C0392B / #E74C3C / #E67E22 / #F5B041)
    # that mixed burden-red with accent-gold and broke the locked palette.
    vmax = float(cat_df[val_col].max()) if len(cat_df) else 1.0
    colors = [
        f"rgba(231, 76, 60, {0.35 + 0.60 * (v / vmax):.2f})"
        for v in cat_df[val_col]
    ]

    # Render Lucide SVG icons inline above the chart — pre-attentive cue for
    # which product category each row represents. Uses a markdown grid instead
    # of overloading Plotly's yaxis ticktext (which doesn't render SVG cleanly).
    icon_row_cols = st.columns(len(cat_df)) if len(cat_df) > 0 else []
    for col, (_, row) in zip(icon_row_cols, cat_df.sort_values(val_col, ascending=False).iterrows()):
        with col:
            st.markdown(
                f'<div style="text-align:center; padding:0.3rem 0;">'
                f'{category_icon_svg(row[cat_col], size=22)}'
                f'<div style="font-size:0.65rem; color:#C0C0C0; margin-top:0.2rem;">{row[cat_col]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    fig4 = go.Figure(go.Bar(
        y=cat_df[cat_col], x=cat_df[val_col],
        orientation="h",
        marker=dict(color=colors),
        text=[f"+{v:.0f}%" for v in cat_df[val_col]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Price increase: +%{x:.1f}%<extra></extra>",
    ))
    fig4.update_layout(
        **CHART_LAYOUT,
        xaxis_title="Price Increase (%)",
        showlegend=False,
    )
    show_chart(fig4, height=400)

    # --- Insight callout ---
    st.markdown(insight_box(
        "The tariff operates as a <b>regressive consumption tax</b>. "
        "Low-income households spend a larger share of their budget on tariffed essentials "
        "(apparel, shoes, food). The bottom decile loses <b>1.14%</b> of income — "
        "3.2x more than the top decile at <b>0.36%</b>. "
        "Even if prices stabilize, the bill has already been paid — disproportionately by those least able to afford it."
    ), unsafe_allow_html=True)
