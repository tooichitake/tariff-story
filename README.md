<div align="center">

# The Tariff Tax — Who Pays?

### A data narrative for the 47th President of the United States

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-Academic%202026-5A5A5A)
![Course](https://img.shields.io/badge/UTS%2036103-AT3%20Data%20Narrative%20Studio-0E1117)

</div>

> **Even if the Fed is right that tariff inflation is a one-time price shift, the bill is still regressive.**
> The bottom income decile loses **1.14% of income**; the top decile, **0.36%**.
> That is a **3.2× gap** — the same policy, and the poorest Americans pay the most.
> The question is not whether to keep the tariffs. The question is who keeps paying for them.

[**▶ Try the Dashboard**](#try-it-in-60-seconds) · [**Read the Four Acts**](#what-youll-see--the-four-acts) · [**Why This Arc**](#why-this-narrative-arc) · [**Data Dictionary**](#data-dictionary) · [**Credits**](#credits)

> **Live Streamlit Cloud URL:** _pending deployment — local run fully supported below._

---

## The 30-Second Version

The United States is running the most aggressive tariff schedule in a century. In 2025 the effective rate climbed from **2.3%** to over **20%** in ninety days, raised **$364 B** in customs duties, and coincided with **83,000 lost manufacturing jobs**. The stakeholder — the President — has a **98-day window** before Section 122 authority expires on **24 July 2026**. This dashboard does not argue for or against tariffs. It makes one claim the political debate has refused to make: *the bill is not split evenly.* Act II is the pivot; everything else sets it up or follows from it.

<div align="center">

| **ACT I** | **ACT II** | **ACT III** | **ACT IV** |
|:---:|:---:|:---:|:---:|
| The Scale | **Who Pays** | What It Bought | The Choice |
| _How big?_ | _Is it fair?_ | _What was the trade-off?_ | _What next?_ |
| Awe · shock | **Empathy · anger** | Complexity · honesty | Urgency · decision |

</div>

---

## Try It in 60 Seconds

**Prerequisites:** Python 3.10 or newer.

```bash
git clone https://github.com/tooichitake/tariff-story.git
cd tariff-story
pip install -r requirements.txt
python run.py
```

Streamlit opens at **http://localhost:8501**. First load takes ~3 seconds — the data is already joined and cached. If something looks wrong, jump to [Troubleshooting](#troubleshooting).

---

## What You'll See — The Four Acts

The dashboard is a single-page vertical scroll. Each act ends where the next begins; the narrator never hands control to the reader until the final slider. The four acts, in order:

### **ACT I — THE SCALE**
*How big is this policy change?*
A dual-axis timeline plots the effective tariff rate against the S&P 500 and the VIX, with every key announcement pinned as a dot. Within 90 days the rate went from under 3% to a century high; every announcement corresponds to a visible fear spike.
**Central viz:** `viz1_tariff_market_fear.csv`

### **ACT II — WHO PAYS** _(the emotional core)_
*Who bears the cost? Is it fair?*
A horizontal bar chart shows annual income lost by decile under two scenarios (Current Policy · IEEPA Upheld). The bottom decile loses 1.14% of income; the top, 0.36%. A 100-person pictogram makes the gap tactile.
**Central viz:** `viz3_who_pays.csv` — the argumentative heart of the project.

### **ACT III — WHAT IT BOUGHT**
*What were the trade-offs?*
Honest, not triumphant. Tariffs generated $364 B in revenue and drove reshoring announcements, but manufacturing employment fell 83K, the trade deficit widened, and the dollar weakened. A scorecard weighs the promises against the outcomes side by side.
**Central viz:** `viz5_manufacturing_tradeoff.csv` + `viz6_world_map.csv`

### **ACT IV — THE CHOICE**
*What should you do, Mr. President?*
A What-If slider lets the reader move the tariff rate between 8% and 17% and watch GDP, jobs, prices, and **distributional burden by decile** update in real time. The yield curve behind it is already inverting.
**Central viz:** `viz7_whatif.csv` + `viz8_recession_signal.csv`

---

## Why This Narrative Arc

> The arc ends with prescription, not exploration — exactly what a 98-day decision demands.

> _Satisfies assignment requirement: "Groups must select **and justify** one of the following narrative structures."_

The rubric offers four arcs. We chose **What → So What → What Next** (the classic executive efficiency arc). Here is why the other three were the wrong fit for this stakeholder:

| Arc | How it works | Why it fails here |
|---|---|---|
| **What → So What → What Next** ← chosen | Headline → stakes → decision | Matches how the President consumes information: briefing-paced, prescription at the end |
| Martini Glass | Author-driven narrative, then a user-sandbox exploration | Hands the President a sandbox they will not use; squanders the urgency built across three acts |
| Detective | Anomaly → clue → culprit | Requires a genuine unknown. Tariff facts are public — there is no "crime" to solve |
| Sparkline | Single gap between *what is* and *what could be* | Collapses four gaps (revenue vs jobs, tariff vs deficit, transitory vs cumulative, bottom vs top decile) into one; hides the core insight |

<details>
<summary><strong>Extended justification (for the graders)</strong></summary>

- The arc's emotional gradient (awe → empathy → complexity → urgency) progressively raises the stakes, so the Act IV countdown lands on a reader who is already informed, not surprised.
- It allows Act III to be **honest** about trade-offs without derailing the argument. The "So What" phase has explicit room for complexity that other arcs collapse.
- The arc concludes with prescription, which matches the stakeholder's job. The President's job is not to explore data; it is to make a defensible decision by 24 July 2026.
- The full stakeholder persona, decision horizon, and user stories driving this choice are documented in [`docs/persona.md`](docs/persona.md).

</details>

---

## Architecture

### Directory

```
tariff-story/
├── .streamlit/config.toml     # Dark theme + server settings (read by Streamlit Cloud)
├── app/                       # Streamlit application
│   ├── app.py                 # Entry — 4 acts + sidebar filter
│   ├── config.py              # Paths, colors, chart defaults
│   ├── data_loader.py         # @st.cache_data loaders
│   ├── styles.py              # Design system — typography, banners, callouts
│   ├── components/            # One module per act + hook
│   │   ├── hook.py
│   │   ├── act1_scale.py
│   │   ├── act2_who_pays.py
│   │   ├── act3_tradeoffs.py
│   │   └── act4_choice.py
│   └── assets/images/         # Narrative imagery (PD / CC0 only)
├── data/
│   ├── raw/                   # Source files (mostly reproducible — see scripts/)
│   ├── cleaned/               # Standardised CSVs (pipeline output)
│   ├── joined/                # 8 viz-ready datasets (viz1..viz8)
│   └── reference/             # key_events.csv + country_mapping.csv
├── scripts/                   # Pipeline 01–14 — run sequentially
├── docs/persona.md            # Stakeholder persona + user stories
├── requirements.txt
├── run.py                     # One-liner launcher
└── README.md
```

### Data flow

```mermaid
flowchart LR
    A[data/raw/<br/>source files] -->|scripts 02, 03, 11| B[data/cleaned/<br/>standardised CSVs]
    B -->|scripts 04, 05, 10, 13, 14| C[data/joined/<br/>viz1..viz8]
    C -->|data_loader.py<br/>@st.cache_data| D[app/<br/>Streamlit UI]
    E[data/reference/<br/>key_events · country_mapping] --> D
```

### Which viz drives which act

| Act | Dataset(s) | Insight carried |
|---|---|---|
| I | `viz1_tariff_market_fear`, `viz6_animated` | Rate × markets × events timeline |
| II | `viz3_who_pays` *(central)*, `viz2_price_pass_through` | Distributional burden by decile |
| III | `viz4_deficit_paradox`, `viz5_manufacturing_tradeoff`, `viz6_world_map`, `viz6_consumer_map` | Trade-offs: revenue ↔ jobs ↔ deficit |
| IV | `viz7_whatif`, `viz8_recession_signal` | Slider scenarios + recession signal |

---

## Reproducing the Pipeline

All scripts use `Path(__file__).resolve().parent.parent` to locate the project root — they are **cross-platform and relocation-safe**, so cloning anywhere works without editing paths.

```bash
python scripts/01_create_priority_data.py      # hardcoded viz3 / viz7 / reference tables
python scripts/02_download_fred.py             # 14 FRED CSVs via HTTP
python scripts/03_download_yale_kaggle.py      # Yale Budget Lab (git clone) + Kaggle (kagglehub)
python scripts/04_clean_all_data.py            # FRED + Yale + Kaggle standardisation
python scripts/04b_fix_kaggle.py               # semicolon-delimiter fix
python scripts/05_create_joins.py              # viz1 / viz2 / viz4 / viz5 / viz6 / viz8
python scripts/10_clean_dfat_gold.py           # DFAT pivot + gold (uses bundled XLSX)
python scripts/11_download_gta_alternatives.py # tradewartracker + White House + Kratosfury
python scripts/13_integrate_gta.py             # enriches daily tariff + world map
python scripts/14_rebuild_data.py              # enhanced viz3 decile parse + viz6 animated
```

**Requirements for full reproduction**

- `scripts/03` uses [`kagglehub`](https://github.com/Kaggle/kagglehub) — needs Kaggle API credentials in `~/.kaggle/kaggle.json`.
- `scripts/10` reads the **DFAT Australia country-commodity pivot** (`data/raw/australia/country-commodity-pivot-table-monthly-series.xlsx`) — this is the **only raw file committed to the repo** because its source (dfat.gov.au) requires browser download.
- All other raw data is excluded by `.gitignore` because the scripts re-download it automatically.

`viz6_consumer_map.csv` is a manual derivation from tradewartracker HS2 tariff data — method documented in `Instructions.md` §25.

---

## Data Dictionary

> _Satisfies assignment requirement: "A mandatory Data Dictionary (definitions of variables, types, and provenance)."_

The app consumes **8 joined datasets** in `data/joined/` plus **2 reference files** in `data/reference/`. Every joined file was produced by merging 2–4 raw sources. All dates are `YYYY-MM-DD`; all country identifiers are ISO 3166 alpha-3.

### Reference files

| Variable | Type | Description | Source |
|---|---|---|---|
| `key_events.date` | date | Event date | Press releases · Fed · SCOTUS |
| `key_events.event_short` | str | ≤ 60-char headline | Editorial |
| `key_events.event_detail` | str | Full narrative description | Editorial |
| `key_events.impact_type` | enum | tariff_up / tariff_down / retaliation / legal / negotiation / threat | Editorial |
| `key_events.eff_tariff_rate_approx` | float | Approximate effective rate on that date (%) | Import-weighted tracker + step function |
| `key_events.story_act` | enum | I / II / III / IV | Editorial (narrative layer) |
| `key_events.source_url` | str | Authoritative URL (WH / Fed / SCOTUS / BLS) | Various |
| `key_events.affected_categories` | str | Product categories (Act II filter) | Editorial |
| `key_events.window_days` | int | Sidebar-filter window for the event | Editorial |
| `key_events.image_path` | str | Event thumbnail path | Wikimedia Commons |
| `country_mapping.name_variant` | str | Alternate country names | Assembled |
| `country_mapping.iso3` | str | Canonical ISO3 | ISO 3166 |

### Joined viz datasets

| File | Rows | Key columns | Source(s) | Used by |
|---|---|---|---|---|
| `viz1_tariff_market_fear.csv` | ~936 daily | date, eff_tariff_rate, sp500, vix, event_short, is_event | tradewartracker + FRED SP500 + VIXCLS + key_events | Act I |
| `viz2_price_pass_through.csv` | monthly | date, eff_tariff_rate, cpi, cpi_yoy, consumer_sentiment | tradewartracker + FRED CPIAUCSL + UMich | Act II |
| `viz3_who_pays.csv` | 20 (10 × 2) | decile, decile_label, scenario, pct_income_lost, usd_cost, most_affected_goods, source | Yale Budget Lab Feb 2026 + TPC cross-check | **Act II (central)**, Act IV slider |
| `viz4_deficit_paradox.csv` | monthly | date, trade_balance, eff_tariff_rate | FRED BOPGSTB + tradewartracker | Act III |
| `viz5_manufacturing_tradeoff.csv` | 27 monthly | date, industrial_prod, unemployment, mfg_employment, mfg_job_openings, eff_tariff_rate | FRED INDPRO + UNRATE + MANEMP + JTS3000JOL | Act III |
| `viz6_world_map.csv` | ~100 | iso3, country_name, tariffs_charged_to_usa, us_reciprocal_tariff, exports, imports, trade_deficit | Kratosfury + White House gist + Kaggle | Act III |
| `viz6_consumer_map.csv` | 57 | iso3, country_name, weighted_tariff_increase, top_category_1/2/3 | Derived — tradewartracker HS2 | Act III |
| `viz6_animated.csv` | country × day | date, iso3, country_name, effective_tariff | tradewartracker daily by-country | Act I |
| `viz7_whatif.csv` | 5 | scenario, eff_tariff_rate, gdp_impact_pct, unemployment_increase_pp, price_increase_pct, household_cost_bottom20_usd, household_cost_top20_usd, tariff_revenue_10yr_trillion, source | Yale Feb/Nov 2026 + TPC | Act IV |
| `viz8_recession_signal.csv` | daily | date, treasury_10y, yield_spread, fed_funds, vix | FRED DGS10 + T10Y2Y + FEDFUNDS + VIXCLS | Act IV |

<details>
<summary><strong>Raw-source inventory</strong> — grouped by provider (click to expand)</summary>

**Primary — feeds the 8 viz CSVs that ship with the app:**

- **Federal Reserve Economic Data (FRED)** — 17 series: SP500, CPIAUCSL, DTWEXBGS, VIXCLS, DGS10, T10Y2Y, A191RL1Q225SBEA (GDP), BOPGSTB, INDPRO, UNRATE, MANEMP, JTS3000JOL, B235RC1Q027SBEA (customs), FEDFUNDS, DCOILWTICO (oil), DEXUSAL (AUD/USD), UMich Consumer Sentiment. https://fred.stlouisfed.org
- **Yale Budget Lab** — Feb 2026 distributional workbook + 7 pre-parsed CSVs + ETR methodology release (HTS basic, IEEPA rates, metal-content shares, MFN rates, NAICS/BEA crosswalks, USMCA product shares). Via `ericrono/Tariff-Aftershock` on GitHub.
- **Tax Policy Center (TPC)** — decile burden cross-check used to validate viz3. https://www.taxpolicycenter.org
- **Kaggle** — `soulaimanebenayad/trump-era-tariffs-by-country-2025-csv-file`, `danielcalvoglez/us-tariffs-2025`, `raza/Trump_tariffs_by_country`
- **Global Trade Alert alternatives** (GTA's official data centre requires login) — `Kratosfury/Tariffs-USA` (57 countries), `mcoliver/gist` White House Liberation Day (126 countries), `tradewartracker/trade-war-redux-2025` (daily tariff + HS2 breakdowns)
- **DFAT Australia** — country-commodity monthly pivot table (17 MB XLSX, committed to the repo), plus related top-25 export/import workbooks. https://www.dfat.gov.au
- **datasets/gold-prices** — monthly gold price (FRED delisted the LBMA series in Jan 2022)

**Acquired for exploration / cross-validation:**

- **Penn Wharton Budget Model (PWBM)** — effective tariff rate estimates. https://budgetmodel.wharton.upenn.edu
- **Bruegel** — Global Trade Tracker. https://www.bruegel.org
- **Federal Reserve Bank of New York** — Survey of Consumer Expectations. https://www.newyorkfed.org
- **Washington Center for Equitable Growth** — US import matrices, tariff industry codes, imports by state. https://equitablegrowth.org
- **Reserve Bank of Australia (RBA)** — cash rate history. https://www.rba.gov.au
- **Australian Bureau of Statistics (ABS)** — merchandise exports/imports. https://www.abs.gov.au
- **US Census Bureau** — Trade by Country tables. https://www.census.gov/foreign-trade
- **Bureau of Labor Statistics (BLS)** — via FRED MANEMP/JTS3000JOL.
- **Bureau of Economic Analysis (BEA)** — via FRED BOPGSTB. https://www.bea.gov

</details>

---

## Deployment

**Local** — `python run.py` (see [Try It in 60 Seconds](#try-it-in-60-seconds)).

**Streamlit Cloud**

1. Push this repository to GitHub.
2. Connect the repo at https://share.streamlit.io.
3. Main file path: `app/app.py` · Python version: 3.11.
4. Paste the deployed URL into the header badge at the top of this README.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'streamlit'` | Virtualenv not activated, or install skipped | `pip install -r requirements.txt` in the active environment |
| `Address already in use` on port 8501 | Another Streamlit instance is running | `streamlit run app/app.py --server.port 8502` |
| `python: command not found` | Python < 3.10 or not on PATH | Install Python 3.10+ and retry |
| Charts render but a dataset is empty | Joined CSV missing — `data/joined/` incomplete | Re-run the [pipeline](#reproducing-the-pipeline) from script 01 |
| "Where does the rubric say X?" | The grader needs a quick meta-nav | Narrative arc → [Why This Narrative Arc](#why-this-narrative-arc) · Data Dictionary → [Data Dictionary](#data-dictionary) · Credits → [Credits](#credits) |

---

## Credits

### Data

- **Federal Reserve Economic Data (FRED)** — https://fred.stlouisfed.org
- **Yale Budget Lab** — distributional analysis, via `ericrono/Tariff-Aftershock`
- **Tax Policy Center** — decile burden cross-check
- **Global Trade Alert alternatives** — `Kratosfury/Tariffs-USA`, `mcoliver/gist`, `tradewartracker/trade-war-redux-2025`
- **Kaggle** — `soulaimanebenayad`, `danielcalvoglez` tariff datasets
- **DFAT Australia** — country-commodity pivot table (manual download, committed)
- **Bureau of Labor Statistics (BLS)** — manufacturing employment (CES/JOLTS)
- **US Census Bureau** — trade flows
- Full 25-source list in `Instructions.md`; each joined CSV carries a `source` column tracking provenance.

### Images (see also [`app/assets/images/LICENSE.md`](app/assets/images/LICENSE.md))

All imagery is Public Domain or CC-licensed — sourced exclusively from Wikimedia Commons. No Getty / AP / Reuters imagery is used.

| File | Source | Licence | Author |
|---|---|---|---|
| `hook_hero.jpg` · `us_china_peak.jpg` | [Wikimedia: Maersk container ships](https://commons.wikimedia.org/wiki/File:MAERSK_MC_KINNEY_M%C3%96LLER_%26_MARSEILLE_MAERSK_(48694054418).jpg) | CC BY-SA 2.0 | Kees Torn (Flickr) |
| `inauguration.jpg` | [Wikimedia: Trump oath of office 2025](https://commons.wikimedia.org/wiki/File:Donald_Trump_takes_the_oath_of_office_(2025)_(alternate).jpg) | Public Domain | The White House |
| `scotus_ruling.jpg` | [Wikimedia: US Supreme Court at dusk](https://commons.wikimedia.org/wiki/File:Panorama_of_United_States_Supreme_Court_Building_at_Dusk.jpg) | Public Domain | Joe Ravi |
| `section_122.jpg` | [Wikimedia: US Capitol](https://commons.wikimedia.org/wiki/File:Capitol_Building_Full_View.jpg) | Public Domain | US Gov / AOC |
| `oval_office.jpg` | [Wikimedia: Oval Office 2017](https://commons.wikimedia.org/wiki/File:View_of_Oval_Office_in_2017.jpg) | Public Domain | Official White House Photo |
| `liberation_day.jpg` | [Wikimedia: Oval Office April 2025](https://commons.wikimedia.org/wiki/File:P20250415JB-0003.jpg) | Public Domain | The White House |
| `geneva_talks.jpg` | [Wikimedia: Palace of Nations conference room](https://commons.wikimedia.org/wiki/File:Conference_Room_in_Palace_of_Nations.jpg) | CC BY-SA | Wikimedia Commons |
| `act2_hands.jpg` | [Wikimedia: Sainsbury's checkout](https://commons.wikimedia.org/wiki/File:Supermarket_check_out.JPG) | Public Domain / CC0 | Wikimedia Commons |

### Fonts

- **Playfair Display** — Claus Eggers Sørensen, [SIL OFL 1.1](https://openfontlicense.org) · Google Fonts CDN · editorial headlines, brand masthead, drop caps.
- **Inter** — Rasmus Andersson, [SIL OFL 1.1](https://openfontlicense.org) · Google Fonts CDN · body text, metric labels, UI chrome.

### Icons

- **[Lucide](https://lucide.dev)** — ISC licence — inline SVGs for product-category labels (Act II), promise/scorecard icons (Act III), the 100-person pictogram seed, and visual-anchor fallbacks.

### Code

| Library | Licence | Use |
|---|---|---|
| [Streamlit](https://streamlit.io) | Apache 2.0 | Web application framework |
| [Plotly](https://plotly.com) | MIT | Charting |
| [pandas](https://pandas.pydata.org) | BSD-3 | Data manipulation |
| [numpy](https://numpy.org) | BSD-3 | Numerical |
| [openpyxl](https://openpyxl.readthedocs.io) | MIT | XLSX reading (DFAT / Yale workbooks) |
| [Pillow](https://python-pillow.org) | MIT-CMU | Image handling (Streamlit internal) |
| [requests](https://requests.readthedocs.io) | Apache 2.0 | HTTP for data pipeline |

---

## Team Contributions

> _Satisfies Part 3 rubric: "observable effort tracking"._

Populated pre-submission. Graders can audit authorship with:

```bash
git log --all --format='%h  %an  %s' --reverse
git shortlog -sn --all
```

---

## License

Academic coursework (**UTS 36103 — MDSI AT3, 2026**). All data remain with their original publishers under their respective licences. See [`app/assets/images/LICENSE.md`](app/assets/images/LICENSE.md) for image provenance and the _Credits_ section above for code and font licences.
