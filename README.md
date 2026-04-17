<div align="center">

# The Tariff Tax — Who Pays?

### A data narrative for the 47th President of the United States

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?logo=plotly&logoColor=white)
![Dashboard](https://img.shields.io/badge/Dashboard-Scrollytelling-F5B041)

</div>

> **Even if the Fed is right that tariff inflation is a one-time price shift, the bill is still regressive.**
> The bottom income decile loses **1.14% of income**; the top decile, **0.36%**.
> That is a **3.2× gap** — the same policy, and the poorest Americans pay the most.
> The question is not whether to keep the tariffs. The question is who keeps paying for them.

[**▶ Try the Dashboard**](#try-it-in-60-seconds) · [**Read the Four Acts**](#what-youll-see--the-four-acts) · [**Why This Arc**](#why-this-narrative-arc) · [**Credits**](#credits)

> **Live Streamlit Cloud URL:** _to be added after deployment — local run fully supported below._

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

Four common narrative structures were considered. **What → So What → What Next** (the classic executive efficiency arc) was chosen for this stakeholder; here is why the others were the wrong fit:

| Arc | How it works | Why it fails here |
|---|---|---|
| **What → So What → What Next** ← chosen | Headline → stakes → decision | Matches how the President consumes information: briefing-paced, prescription at the end |
| Martini Glass | Author-driven narrative, then a user-sandbox exploration | Hands the President a sandbox they will not use; squanders the urgency built across three acts |
| Detective | Anomaly → clue → culprit | Requires a genuine unknown. Tariff facts are public — there is no "crime" to solve |
| Sparkline | Single gap between *what is* and *what could be* | Collapses four gaps (revenue vs jobs, tariff vs deficit, transitory vs cumulative, bottom vs top decile) into one; hides the core insight |

The arc's emotional gradient — awe → empathy → complexity → urgency — progressively raises the stakes, so the Act IV countdown lands on a reader who is already informed, not surprised. It also lets Act III be honest about trade-offs without derailing the argument; the "So What" phase has explicit room for complexity that other arcs collapse. The full stakeholder persona and user stories are in [`docs/persona.md`](docs/persona.md).

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
    A["data/raw/<br/>source files"] -->|"scripts 02, 03, 11"| B["data/cleaned/<br/>standardised CSVs"]
    B -->|"scripts 04, 05, 10, 13, 14"| C["data/joined/<br/>viz1-viz8"]
    C -->|"data_loader.py<br/>@st.cache_data"| D["app/<br/>Streamlit UI"]
    E["data/reference/<br/>key_events · country_mapping"] --> D
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

`viz6_consumer_map.csv` is a manual derivation from tradewartracker HS2 tariff data.

---

## Datasets

The app consumes eight joined CSVs in `data/joined/` plus two reference files in `data/reference/`. All dates are `YYYY-MM-DD`; country identifiers are ISO 3166 alpha-3. Every joined CSV carries a `source` column tracking provenance.

| File | What it shows | Act |
|---|---|---|
| `viz1_tariff_market_fear` | Daily tariff rate × S&P 500 × VIX × event pins | I |
| `viz6_animated` | Tariff rate by country over time (animated map) | I |
| `viz2_price_pass_through` | Monthly tariff × CPI × consumer sentiment | II |
| `viz3_who_pays` | Decile income loss — two policy scenarios | **II (central)**, IV slider |
| `viz4_deficit_paradox` | Monthly trade balance × tariff rate | III |
| `viz5_manufacturing_tradeoff` | Industrial production × employment × job openings | III |
| `viz6_world_map` | Country-level tariffs + reciprocal + trade flows | III |
| `viz6_consumer_map` | Per-country tariff increase weighted by consumer goods | III |
| `viz7_whatif` | Five tariff scenarios (GDP, jobs, prices, revenue) | IV |
| `viz8_recession_signal` | 10Y Treasury · 2Y-10Y spread · fed funds · VIX | IV |

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
- Each joined CSV carries a `source` column tracking provenance.

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

## License

Data and media remain with their original publishers under their respective licences — see [`app/assets/images/LICENSE.md`](app/assets/images/LICENSE.md) for image provenance, and the _Credits_ section above for code, font, and data licences.
