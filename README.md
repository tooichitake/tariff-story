# The Tariff Tax — Who Pays?

**A Data Narrative for the President of the United States**
_AT3: The Data Narrative Studio | UTS MDSI | 2026_

> Even if tariff inflation is a one-time price shift (the Fed's base case), the bill is **regressive**: the bottom income decile loses **1.14%** of income, the top decile **0.36%** — a **3.2x gap**. The question isn't whether to keep the tariffs. The question is whether the poorest Americans should keep paying the most for them.

[▶ Live Dashboard](#) _(Streamlit Cloud URL — to be added after deployment)_ · [Persona & User Stories](docs/persona.md) · [Narrative Arc Justification](#narrative-arc--justification) · [Data Dictionary](#data-dictionary) · [Credits](#credits)

---

## Quick Start

```bash
# 1. Install
pip install -r requirements.txt

# 2. Run locally
python run.py
# or
streamlit run app/app.py
```

Requires Python 3.10+.

---

## Project Overview

**Stakeholder**: President of the United States
**Decision horizon**: 98 days (Section 122 authority expires 2026-07-24)
**Format**: Streamlit scrollytelling dashboard, 4 narrative acts
**Data sources**: 25 datasets (FRED, Yale Budget Lab, Kaggle, Global Trade Alert alternatives, DFAT Australia, BLS, US Census)
**Joined datasets**: 8 viz-ready CSVs (viz1..viz8)
**Advanced features** (rubric requires ≥3): (1) What-If Parameterization · (2) Context-Aware Event Filtering · (3) Narrative Scrollytelling · (4) Rich Tooltips

### Narrative Structure

| Act | Arc role | Title | Core question | Emotional beat |
|---|---|---|---|---|
| I | WHAT | The Scale | How big is this policy change? | Awe / shock |
| II | SO WHAT | Who Pays | Who bears the cost? Is it fair? | Empathy |
| III | SO WHAT | What Did It Buy | What were the trade-offs? | Complexity / honesty |
| IV | WHAT NEXT | The Choice | What should you do, Mr. President? | Urgency |

---

## Narrative Arc & Justification

_(This section satisfies assignment_requirements.txt line 42: "Groups must select **and justify** one of the following narrative structures.")_

### Why We Chose **What → So What → What Next** (the classic executive efficiency arc)

Our stakeholder is the President of the United States. They read at the pace of a briefing memo: headline, stakes, decision — in that order. A narrative arc must match how they consume information, not how analysts want to tell it.

**Why not the Martini Glass** (author-driven → user sandbox):
The Martini Glass hands the user a sandbox at the end. The President is not going to explore filters; they are going to make a decision. Dropping them into an open sandbox after Act III would squander the urgency we have spent three acts building.

**Why not the Detective** (anomaly → culprit):
The Detective requires a genuine unknown at the start. The tariff facts are fully public — the President already knows the rate went up. There is no "crime" to solve, only a question of distributional fairness to confront. Framing this as detective-work would feel manipulative.

**Why not the Sparkline** (what is vs. what could be):
The Sparkline highlights a single gap. Our story has four gaps (revenue vs. jobs, tariff up vs. deficit behavior, Fed's transitory view vs. cumulative burden, bottom decile vs. top decile). Collapsing them into one would hide the core insight: the policy has real gains and real costs — refusing either side is the mistake.

**Why What → So What → What Next fits**:
- The arc ends with prescription, not exploration — which is exactly what a 98-day decision horizon demands.
- The emotional gradient (awe → empathy → complexity → urgency) progressively raises the stakes, so the final Act IV countdown lands on a viewer who is already informed, not surprised.
- It allows Act III to be honest about trade-offs without derailing the argument — the "So What" phase has explicit room for complexity that other arcs collapse.

---

## Architecture

```
tariff-story/
├── app/                       # Streamlit application
│   ├── app.py                 # Main entry — 4 acts + sidebar filter
│   ├── config.py              # Paths, colors, chart defaults
│   ├── data_loader.py         # @st.cache_data loaders for all viz CSVs
│   ├── styles.py              # Design system: typography, act banners, callouts, helpers
│   ├── components/            # One module per act (plus hook)
│   │   ├── hook.py
│   │   ├── act1_scale.py
│   │   ├── act2_who_pays.py
│   │   ├── act3_tradeoffs.py
│   │   └── act4_choice.py
│   ├── assets/
│   │   └── images/            # Narrative imagery (PD/CC0 only — see LICENSE.md)
│   └── .streamlit/config.toml # Dark theme
├── data/
│   ├── raw/                   # Untouched source CSVs
│   ├── cleaned/               # Standardized CSVs
│   ├── joined/                # 8 viz-ready datasets (viz1..viz8)
│   └── reference/             # key_events.csv, country_mapping.csv
├── scripts/                   # Data pipeline (01..14 — run sequentially)
├── docs/
│   └── persona.md             # Stakeholder persona + user stories + AC/DoD
├── requirements.txt
├── run.py                     # One-liner launcher
└── README.md
```

---

## Deployment

### Local

```bash
python run.py
```

### Streamlit Cloud

1. Push this repository to GitHub.
2. At https://share.streamlit.io, connect the repo.
3. Main file path: `app/app.py`.
4. Python version: 3.11.
5. The URL will be added to the header of this README.

---

## Data Dictionary

_(This section satisfies assignment_requirements.txt line 77: "a mandatory Data Dictionary (definitions of variables, types, and provenance)".)_

The app consumes **8 joined datasets** in `data/joined/` (viz1..viz8) plus 2 reference files in `data/reference/`. Each joined file was produced by joining 2–4 raw sources. All temporal data is normalised to `YYYY-MM-DD`; country identifiers use ISO 3166 alpha-3.

### Reference files

| Variable | Type | Description | Source |
|---|---|---|---|
| `key_events.date` | date | Event date (YYYY-MM-DD) | Assembled from press releases + Fed + SCOTUS |
| `key_events.event_short` | str | ≤ 60 char headline | Editorial |
| `key_events.event_detail` | str | Full narrative description | Editorial |
| `key_events.impact_type` | enum | tariff_up / tariff_down / retaliation / legal / negotiation / threat | Editorial |
| `key_events.eff_tariff_rate_approx` | float | Approximate effective rate on that date (%) | Import-weighted tracker + step function |
| `key_events.story_act` | enum | I / II / III / IV | Editorial (narrative layer) |
| `key_events.source_url` | str | Authoritative URL for the claim (WH / Fed / SCOTUS / BLS / etc.) | Various — see column |
| `key_events.affected_categories` | str | Comma-separated product categories (Act II filter) | Editorial |
| `key_events.window_days` | int | Window used when the event is selected in the sidebar filter | Editorial |
| `key_events.image_path` | str | Relative path to event thumbnail (H3) | Wikimedia Commons (see `app/assets/images/LICENSE.md`) |
| `country_mapping.name_variant` | str | Alternate country names | Assembled |
| `country_mapping.iso3` | str | Canonical ISO3 | ISO 3166 |

### Joined viz datasets

| File | Rows | Key columns | Source(s) | Used by |
|---|---|---|---|---|
| `viz1_tariff_market_fear.csv` | ~936 daily | date, eff_tariff_rate, sp500, vix, event_short, is_event | tradewartracker daily_tariff + key_events step + FRED SP500 + FRED VIXCLS | Act I |
| `viz2_price_pass_through.csv` | monthly | date, eff_tariff_rate, cpi, cpi_yoy, consumer_sentiment | tradewartracker + FRED CPIAUCSL + UMich sentiment | Act II (reserved) |
| `viz3_who_pays.csv` | 20 (10 deciles × 2 scenarios) | decile, decile_label, scenario, pct_income_lost, usd_cost, most_affected_goods, source | Yale Budget Lab Feb 2026 + TPC tariff tracker (cross-check) | Act II (central), Act IV (slider interpolation) |
| `viz4_deficit_paradox.csv` | monthly | date, trade_balance, eff_tariff_rate | FRED BOPGSTB + tradewartracker | Act III |
| `viz5_manufacturing_tradeoff.csv` | 27 monthly | date, industrial_prod, unemployment, mfg_employment, mfg_job_openings, eff_tariff_rate | FRED INDPRO + UNRATE + MANEMP + JTS3000JOL + tradewartracker | Act III |
| `viz6_world_map.csv` | ~100 | iso3, country_name, tariffs_charged_to_usa, us_reciprocal_tariff, exports, imports, trade_deficit | Kratosfury/Tariffs-USA + White House Liberation Day gist + Kaggle | Act III |
| `viz6_consumer_map.csv` | 57 | iso3, country_name, weighted_tariff_increase, top_category_1/2/3 | Derived from tradewartracker HS2 tariff files (manual join, documented in Instructions.md §25) | Act III |
| `viz6_animated.csv` | country × day | date, date_str, iso3, country_name, effective_tariff | tradewartracker daily by-country tariffs | Act I |
| `viz7_whatif.csv` | 5 | scenario, eff_tariff_rate, gdp_impact_pct, unemployment_increase_pp, price_increase_pct, household_cost_bottom20_usd, household_cost_top20_usd, tariff_revenue_10yr_trillion, source | Yale Budget Lab Feb/Nov 2026 distributional reports + TPC estimates | Act IV |
| `viz8_recession_signal.csv` | daily | date, treasury_10y, yield_spread, fed_funds, vix | FRED DGS10 + T10Y2Y + FEDFUNDS + VIXCLS | Act IV |

### Raw-source inventory

Grouped by provider. Some are used directly by the shipped app; others were acquired for exploration / cross-validation and are retained in `data/raw/` for reproducibility.

**Primary (feed the 8 viz CSVs used by the app):**

- **Federal Reserve Economic Data (FRED)** — 17 series retrieved: SP500, CPIAUCSL, DTWEXBGS, VIXCLS, DGS10, T10Y2Y, A191RL1Q225SBEA (GDP), BOPGSTB, INDPRO, UNRATE, MANEMP, JTS3000JOL, B235RC1Q027SBEA (customs), FEDFUNDS, DCOILWTICO (oil), DEXUSAL (AUD/USD), plus UMich Consumer Sentiment. https://fred.stlouisfed.org
- **Yale Budget Lab** — February 2026 tariff distributional workbook + 7 pre-parsed CSVs (commodity prices, country GDP, regional tariffs, revenue forecast/projections, sectoral GDP, summary metrics). Also their full ETR methodology release (`etr_*` files: HTS basic edition, IEEPA rates, metal content shares, MFN rates, NAICS/BEA crosswalks, USMCA product shares). Via `ericrono/Tariff-Aftershock` on GitHub.
- **Tax Policy Center (TPC)** — decile burden cross-check used to validate viz3. https://www.taxpolicycenter.org
- **Kaggle** — `soulaimanebenayad/trump-era-tariffs-by-country-2025-csv-file`, `danielcalvoglez/us-tariffs-2025`, `raza/Trump_tariffs_by_country`
- **Global Trade Alert alternatives** (GTA's official data centre requires login) — `Kratosfury/Tariffs-USA` (57 countries), `mcoliver/gist` White House Liberation Day (126 countries), `tradewartracker/trade-war-redux-2025` (daily tariff + HS2 breakdowns)
- **DFAT Australia** — country-commodity monthly pivot table (17 MB XLSX), plus related top-25 export/import workbooks and trade factsheets. https://www.dfat.gov.au
- **datasets/gold-prices** — monthly gold price (FRED delisted the LBMA series in Jan 2022)

**Acquired for exploration, retained in `data/raw/` for reproducibility:**

- **Penn Wharton Budget Model (PWBM)** — effective tariff rate estimates workbook. https://budgetmodel.wharton.upenn.edu
- **Bruegel** — Global Trade Tracker. https://www.bruegel.org
- **Federal Reserve Bank of New York** — Survey of Consumer Expectations (inflation-expectations workbook). https://www.newyorkfed.org
- **Washington Center for Equitable Growth** — US import matrices, tariff industry codes, US imports by state (2017 / 2024). https://equitablegrowth.org
- **Reserve Bank of Australia (RBA)** — cash rate history. https://www.rba.gov.au
- **Australian Bureau of Statistics (ABS)** — merchandise exports/imports (all countries). https://www.abs.gov.au
- **US Census Bureau** — Trade by Country tables. https://www.census.gov/foreign-trade
- **Bureau of Labor Statistics (BLS)** — via FRED MANEMP/JTS3000JOL; event narrative cites their CES release directly.
- **Bureau of Economic Analysis (BEA)** — via FRED BOPGSTB; trade-balance methodology. https://www.bea.gov

---

## Credits

### Data Sources

See **Dataset Inventory** in `Instructions.md` for the full 25-source list. Each joined CSV has a `source` column tracking provenance.

Primary authoritative sources:
- **Federal Reserve Economic Data (FRED)** — https://fred.stlouisfed.org
- **Yale Budget Lab** — distributional analysis, via `ericrono/Tariff-Aftershock`
- **Tax Policy Center** — decile burden cross-check
- **Global Trade Alert alternatives** — `Kratosfury/Tariffs-USA`, White House gist, `tradewartracker/trade-war-redux-2025`
- **Kaggle** — `soulaimanebenayad`, `danielcalvoglez` tariff datasets
- **DFAT Australia** — country-commodity pivot table (manual download)
- **Bureau of Labor Statistics (BLS)** — manufacturing employment (CES/JOLTS)
- **US Census Bureau** — trade flows

### Images (see also `app/assets/images/LICENSE.md`)

All imagery is Public Domain or CC-licenced — sourced exclusively from Wikimedia Commons. No Getty / AP / Reuters imagery is used.

| File | Source | Licence | Author |
|---|---|---|---|
| `hook_hero.jpg` | [Wikimedia: Maersk container ships](https://commons.wikimedia.org/wiki/File:MAERSK_MC_KINNEY_M%C3%96LLER_%26_MARSEILLE_MAERSK_(48694054418).jpg) | CC BY-SA 2.0 | Kees Torn (Flickr) |
| `us_china_peak.jpg` | same as above | CC BY-SA 2.0 | Kees Torn (Flickr) |
| `inauguration.jpg` | [Wikimedia: Trump oath of office 2025](https://commons.wikimedia.org/wiki/File:Donald_Trump_takes_the_oath_of_office_(2025)_(alternate).jpg) | Public Domain | The White House |
| `scotus_ruling.jpg` | [Wikimedia: US Supreme Court at dusk](https://commons.wikimedia.org/wiki/File:Panorama_of_United_States_Supreme_Court_Building_at_Dusk.jpg) | Public Domain | Joe Ravi |
| `section_122.jpg` | [Wikimedia: US Capitol](https://commons.wikimedia.org/wiki/File:Capitol_Building_Full_View.jpg) | Public Domain | US Gov / AOC |
| `oval_office.jpg` | [Wikimedia: Oval Office 2017](https://commons.wikimedia.org/wiki/File:View_of_Oval_Office_in_2017.jpg) | Public Domain | Official White House Photo |
| `liberation_day.jpg` | [Wikimedia: Oval Office April 2025](https://commons.wikimedia.org/wiki/File:P20250415JB-0003.jpg) | Public Domain | The White House |
| `geneva_talks.jpg` | [Wikimedia: Palace of Nations conference room](https://commons.wikimedia.org/wiki/File:Conference_Room_in_Palace_of_Nations.jpg) | CC BY-SA | Wikimedia Commons contributor |
| `act2_hands.jpg` | [Wikimedia: Sainsbury's checkout](https://commons.wikimedia.org/wiki/File:Supermarket_check_out.JPG) | Public Domain / CC0 | Wikimedia Commons contributor |

### Icons

- [Lucide](https://lucide.dev) SVG icons inlined in the app — MIT licence — used for product categories (Act II viz4), scorecard rows (Act III), and fallback illustrations on visual anchors when a hero image is absent.

### Code

- [Streamlit](https://streamlit.io) — Apache 2.0 (web application framework)
- [Plotly](https://plotly.com) — MIT (charting)
- [pandas](https://pandas.pydata.org) — BSD-3 (data manipulation)
- [numpy](https://numpy.org) — BSD-3 (numerical)
- [openpyxl](https://openpyxl.readthedocs.io) — MIT (XLSX reading)
- [Pillow](https://python-pillow.org) — MIT-CMU (image handling)
- [requests](https://requests.readthedocs.io) — Apache 2.0 (HTTP for data pipeline)

### Icons

- [Lucide](https://lucide.dev) — ISC licence — inlined SVG set used for product-category labels in Act II viz4, promise/scorecard icons in Act III, the 100-person pictogram seed icon, and fallback illustrations on visual anchors when a hero image is absent.

### Fonts

- **Playfair Display** — designed by Claus Eggers Sørensen. [SIL Open Font License 1.1](https://openfontlicense.org). Loaded from Google Fonts CDN. Used for editorial headlines, brand masthead, scorecard title, and drop caps.
- **Inter** — designed by Rasmus Andersson. [SIL Open Font License 1.1](https://openfontlicense.org). Loaded from Google Fonts CDN. Used for body text, metric labels, navigation, and UI chrome.

---

## Team Contributions

_(Part 3 rubric mandates observable effort tracking — populated pre-submission via `git log` and commit attribution.)_

---

## Reproducing the Data

```bash
# Run the pipeline scripts sequentially (they currently hardcode Windows paths —
# adjust BASE_DIR at the top of each script for other platforms).
python scripts/01_create_priority_data.py
python scripts/02_download_fred.py
python scripts/03_download_yale_kaggle.py
python scripts/04_clean_all_data.py
python scripts/05_create_joins.py
# ... through to scripts/14_rebuild_data.py
```

`viz6_consumer_map.csv` is a manual derivation from `tradewartracker/trade-war-redux-2025` HS2 tariff data — see `Instructions.md` Dataset Inventory entry #25 for method notes.

---

## License

Academic coursework (UTS 36103 MDSI AT3, 2026). Data remain with their original publishers under their respective licenses.
