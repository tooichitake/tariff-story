"""Act II: WHO PAYS — The emotional core of the narrative.
Viz 3: 10-decile income burden (horizontal bar, scenario toggle)
Viz 4: Price impact by category (horizontal bar)
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from config import COLORS, DECILE_COLORS, CHART_LAYOUT, show_chart
from styles import (
    chart_header, insight_box, styled_metric_card, visual_anchor, act_intro,
    category_icon_svg, ASSETS_DIR,
)


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

    # --- Viz 3: 10-Decile Income Burden (CENTRAL VISUALIZATION) ---
    st.markdown(chart_header(
        "The Poorest Lose 3x More of Their Income",
        "Tariff burden as percentage of post-tax income, by household income decile"
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

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        y=[f"Decile {d}" for d in data["decile"]],
        x=data[y_col],
        orientation="h",
        marker=dict(color=DECILE_COLORS),
        text=[f"{v:.2f}%" if view == "% of Income" else f"${v:,.0f}" for v in data[y_col]],
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            + ("Income Lost: %{x:.2f}%" if view == "% of Income" else "Cost: $%{x:,.0f}")
            + "<br>Goods: %{customdata}<extra></extra>"
        ),
        customdata=data["most_affected_goods"],
    ))

    # Gap annotation
    if view == "% of Income":
        fig3.add_annotation(
            x=max(data[y_col]) * 1.25, y="Decile 5",
            text=f"<b>{d1_pct / d10_pct:.1f}x</b><br><span style='font-size:10px'>gap</span>",
            showarrow=False,
            font=dict(size=20, color=COLORS["accent_red"]),
        )

    fig3.update_layout(
        **CHART_LAYOUT,
        xaxis_title=x_label,
        yaxis=dict(autorange="reversed"),
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
