# Claude Code Instructions — AT3 Tariff War Data Story
# "The Tariff Tax: Who Pays?"

---

## Project Context (READ FIRST)

**University project**: AT3: The Data Narrative Studio (40% of grade)
**Topic**: Trump's 2025 Tariff War
**Stakeholder**: US President
**Core Story**: "The Tariff Tax: Who Pays?" — Even if tariff inflation is a one-time price shift (the Fed's base case), the burden is distributed regressively: bottom income decile loses **1.14%** of income, top decile loses **0.36%** — a **3.2x gap**. (Source: Yale Budget Lab distributional analysis, Feb 2026; see `data/joined/viz3_who_pays.csv`.)
**Tool**: Streamlit (Python) or Tableau Public
**Grading**: DI/HD path requires joining multiple datasets

### Narrative Arc — What → So What → What Next

**Structure**: The classic executive efficiency arc. The entire dashboard is author-driven — the narrator controls the argument from start to finish, ending with a clear recommendation.

| Act | Arc Role | Title | Core Question | Emotion |
|-----|----------|-------|---------------|---------|
| I | **WHAT** | THE SCALE | How big is this policy change? | Awe / shock at speed and magnitude |
| II | **SO WHAT** | WHO PAYS | Who bears the cost? Is it fair? | Empathy / anger at inequality |
| III | **SO WHAT** | WHAT DID IT BUY | What were the trade-offs? | Complexity / honest uncertainty |
| IV | **WHAT NEXT** | THE CHOICE | What should you do? | Urgency / decision |

**Why this arc (not Martini Glass)**: Our stakeholder is the US President — they need a briefing that acknowledges achievements, reveals the hidden cost, and drives action. The What-If comparison in Act IV shows the distributional burden under each policy path, reinforcing the core story: "who pays?" The narrator maintains control throughout, guiding the President to confront the fairness question.

### Key Narrative Principle
- Act II is the emotional core — distributional unfairness is the central insight
- Act III must be HONEST — acknowledge gains (reshoring investment up, tariff revenue, negotiating leverage) alongside costs (jobs down, deficit paradox)
- Proactively address the Fed's "transitory" view in Act II: "Even if this is a one-time price shift, the bill is still unfair"
- Act IV does NOT recommend removing tariffs — it acknowledges what tariffs achieved, then asks "who is paying for it?" The call to action is to **fix the distribution**, not abandon the policy. The closing message: "The tariff generated $364B. The question isn't whether to keep it. The question is whether the poorest Americans should keep paying the most."

### Key Deadlines
- Part 1 due: April 19, 2026 (individual, binary grading)
- Part 2 Presentation: May 13, 2026 (group, 10 min + Q&A)
- Part 3 Final Portfolio: May 17, 2026 (group, deployed dashboard + video + docs)

---

## Dataset Inventory

### Acquired Datasets — Actual Sources Used

| # | Dataset | Source | File Location | Purpose | Act |
|---|---------|--------|--------------|---------|-----|
| 1 | **Daily Tariff Rate** | tradewartracker/trade-war-redux-2025 (GitHub) | `data/raw/other/tradewar_daily_tariff.csv` | Import-weighted daily effective tariff rate (176 days, 2.3%–30.2%) | All |
| 2 | Yale Budget Lab XLSX | ericrono/Tariff-Aftershock (GitHub) | `data/raw/yale/TBL-Data-February-Tariffs-202602_0.xlsx` | 10 sheets: distributional (F5), regional tariffs (T2), commodity prices (F6), GDP (F2), revenue (T3) | I–IV |
| 3 | Yale Budget Lab CSVs | same repo, pre-parsed | `data/raw/yale/output_*.csv` (7 files) | Commodity prices, country GDP, regional tariffs, revenue, sectoral GDP, summary | I–IV |
| 4 | TPC/Yale Distributional | Hardcoded from TPC Tariff Tracker + Yale reports | `data/joined/viz3_who_pays.csv` | Income quintile burden — **CENTRAL VISUALIZATION** | II |
| 5 | **GTA Country Tariffs** | Kratosfury/Tariffs-USA (GitHub) | `data/raw/other/gta_tariffs_usa.xlsx` | 57 countries: exports, imports, trade deficit, reciprocal tariff rates | I, III |
| 6 | **White House Liberation Day** | mcoliver/gist (GitHub) | `data/raw/other/whitehouse_trump_tariffs_20250402.csv` | 126 countries: tariffs charged to USA + US reciprocal tariffs (Apr 2, 2025) | I, III |
| 7 | Kaggle Trump Tariffs | soulaimanebenayad/trump-era-tariffs-by-country-2025 | `data/raw/kaggle/Trump_tariffs_by_country.csv` | 185 countries: tariff rates charged to USA + reciprocal | I, III |
| 8 | Kaggle US Tariffs 2025 | danielcalvoglez/us-tariffs-2025 | `data/raw/kaggle/Tariff Calculations*.csv` (2 files) | 204 countries: deficit, exports, imports, population | III |
| 9 | FRED S&P 500 | FRED CSV (SP500) | `data/raw/fred/sp500.csv` | Daily stock market reaction | I, II |
| 10 | FRED CPI | FRED CSV (CPIAUCSL) | `data/raw/fred/cpi.csv` | Monthly consumer prices | II |
| 11 | FRED USD Index | FRED CSV (DTWEXBGS) | `data/raw/fred/usd_index.csv` | Daily dollar strength | III |
| 12 | FRED Gold Price | datasets/gold-prices (GitHub) | `data/raw/fred/gold.csv` | Monthly gold price (FRED delisted LBMA Gold in Jan 2022) | III |
| 13 | FRED VIX | FRED CSV (VIXCLS) | `data/raw/fred/vix.csv` | Daily fear/panic index | I, II |
| 14 | FRED 10Y Treasury | FRED CSV (DGS10) | `data/raw/fred/treasury_10y.csv` | Daily inflation/recession signal | III, IV |
| 15 | FRED GDP Growth | FRED CSV (A191RL1Q225SBEA) | `data/raw/fred/gdp_growth.csv` | Quarterly real GDP growth | III |
| 16 | FRED Trade Balance | FRED CSV (BOPGSTB) | `data/raw/fred/trade_balance.csv` | Monthly trade deficit paradox | III |
| 17 | FRED Industrial Production | FRED CSV (INDPRO) | `data/raw/fred/industrial_prod.csv` | Monthly manufacturing index | III |
| 18 | FRED Unemployment | FRED CSV (UNRATE) | `data/raw/fred/unemployment.csv` | Monthly unemployment rate | II, III |
| 19 | FRED 2Y-10Y Yield Spread | FRED CSV (T10Y2Y) | `data/raw/fred/yield_spread.csv` | Daily recession signal | IV |
| 20 | **DFAT SITC Monthly** | dfat.gov.au (manual download) | `data/raw/australia/country-commodity-pivot-table-monthly-series.xlsx` | 17MB pivot table: 265 SITC commodities × 50 months (Jan 2022–Feb 2026), AUD thousands | III |
| 21 | Trade War Tracker extras | tradewartracker (GitHub) | `data/raw/other/tradewar_*.csv` (9 files) | Canada/China/EU export detail, federal tax duty, NIPA imports, country mapping | III |
| 22 | **FRED Mfg Employment** | FRED CSV (MANEMP) | `data/raw/fred/mfg_employment.csv` | Monthly manufacturing employment (thousands, 27 rows, 12,576–12,875K) | III |
| 23 | **FRED Mfg Job Openings** | FRED CSV (JTS3000JOL) | `data/raw/fred/mfg_job_openings.csv` | Monthly JOLTS manufacturing openings (thousands, 26 rows, 376–557K) | III |
| 24 | **FRED Customs Duties** | FRED CSV (B235RC1Q027SBEA) | `data/raw/fred/customs_duties.csv` | Quarterly customs duties revenue (SAAR, $82–364B) | III, IV |
| 25 | **Consumer Goods Map** | Derived from tradewar HS2 tariff files | `data/joined/viz6_consumer_map.csv` | 57 countries: weighted tariff increase on consumer goods (electronics, clothing, toys) with top 3 categories | III |

### Data Source Notes

- **GTA official site** (globaltradealert.org) requires browser login; replaced with GitHub alternatives that cover the same country-level tariff data
- **FRED Gold Price** (LBMA series) was removed from FRED on Jan 31, 2022 (ICE Benchmark Administration data withdrawal); replaced with datasets/gold-prices GitHub repo (monthly)
- **Yale daily tariff rate tracker** not separately available; replaced with tradewartracker daily_tariff.csv (import-weighted average, Jan–Jun 2025) + key_events step function (Jul 2025–Jul 2026)
- **ABS Australia-US bilateral** not downloadable via API; DFAT SITC pivot table covers Australian total trade by commodity (gold = SITC 971, 3rd largest export at A$144B)

---

## Directory Structure

```
tariff-story/                            # Project root
├── app/                                 # Streamlit application
│   ├── app.py                           # Main entry point
│   ├── config.py                        # Colors, paths, constants
│   ├── data_loader.py                   # @st.cache_data loaders
│   ├── components/                      # 4-act visualization modules
│   │   ├── act1_scale.py
│   │   ├── act2_who_pays.py
│   │   ├── act3_tradeoffs.py
│   │   └── act4_choice.py
│   └── .streamlit/config.toml           # Dark theme
├── data/
│   ├── raw/
│   │   ├── fred/                        # 11 FRED CSV files
│   │   ├── kaggle/                      # 3 Kaggle CSV files
│   │   ├── yale/                        # 1 XLSX + 7 CSV from Yale
│   │   ├── australia/                   # DFAT SITC pivot table (17MB)
│   │   └── other/                       # GTA alternatives + trade war tracker (12 files)
│   ├── cleaned/                         # 25 standardized CSV files
│   ├── joined/                          # 8 visualization datasets (viz1–viz8)
│   └── reference/                       # key_events.csv + country_mapping.csv
├── scripts/                             # Data pipeline scripts (01–13)
├── notebooks/
├── docs/
├── requirements.txt
├── Claude_Code_Instructions_EN.md
├── Tariff_Timeline_EN.md
├── assignment_requirements.txt
└── AT3_Complete_Dataset_Inventory_EN.xlsx
```

---

## Task 1: Download FRED Data (10 series + gold alternative)

**FRED CSV endpoint**: `https://fred.stlouisfed.org/graph/fredgraph.csv?id={ID}&cosd=2024-01-01&coed=2026-04-08`
**Script**: `scripts/02_download_fred.py`

| File | Series ID | Freq | Act | Status |
|------|-----------|------|-----|--------|
| sp500.csv | SP500 | Daily | I, II | OK (591 rows) |
| cpi.csv | CPIAUCSL | Monthly | II | OK (26 rows) |
| usd_index.csv | DTWEXBGS | Daily | III | OK (589 rows) |
| vix.csv | VIXCLS | Daily | I, II | OK (590 rows) |
| treasury_10y.csv | DGS10 | Daily | III, IV | OK (590 rows) |
| yield_spread.csv | T10Y2Y | Daily | IV | OK (591 rows) |
| gdp_growth.csv | A191RL1Q225SBEA | Quarterly | III | OK (8 rows) |
| trade_balance.csv | BOPGSTB | Monthly | III | OK (26 rows) |
| industrial_prod.csv | INDPRO | Monthly | III | OK (26 rows) |
| unemployment.csv | UNRATE | Monthly | II, III | OK (27 rows) |
| gold.csv | datasets/gold-prices (GitHub) | Monthly | III | OK (27 rows, $2,050–$5,020) |
| mfg_employment.csv | MANEMP | Monthly | III | OK (27 rows, 12,576–12,875K) |
| mfg_job_openings.csv | JTS3000JOL | Monthly | III | OK (26 rows, 376–557K) |
| customs_duties.csv | B235RC1Q027SBEA | Quarterly | III, IV | OK (8 rows, $82–364B) |

**Note**: FRED LBMA Gold (GOLDPMGBD228NLBM) was removed Jan 31, 2022. Gold price sourced from `github.com/datasets/gold-prices` monthly dataset.

---

## Task 2: Tariff Policy Data

**2A — Kaggle** (automated via `kagglehub`): `scripts/03_download_yale_kaggle.py`
1. `soulaimanebenayad/trump-era-tariffs-by-country-2025-csv-file` → 185 countries
2. `danielcalvoglez/us-tariffs-2025` → 204 countries with deficit/exports/imports/population

**2B — Yale Budget Lab** (GitHub clone): `scripts/03_download_yale_kaggle.py`
- `git clone https://github.com/ericrono/Tariff-Aftershock.git` → XLSX + 7 pre-parsed CSVs
- XLSX sheets: Data TOC, T1 (summary), T2 (regional tariffs), F1 (historical rate), F2 (GDP), F3 (sectoral GDP), T3 (revenue), F5 (distributional), F6 (commodity prices)

**2C — GTA alternatives** (GitHub): `scripts/11_download_gta_alternatives.py`
- `Kratosfury/Tariffs-USA` → 57 countries with export/import/deficit/reciprocal tariff + elasticity
- `mcoliver/gist` White House Liberation Day tariffs → 126 countries (Apr 2, 2025 announcement)
- `tradewartracker/trade-war-redux-2025` → **daily import-weighted avg tariff rate** (176 days) + Canada/China/EU export breakdowns + federal tax duty + NIPA imports

**Note**: GTA official site (globaltradealert.org) requires browser login for data center. The three GitHub sources above cover equivalent country-level and daily tariff data.

---

## Task 3: Australian Data

- **DFAT SITC Monthly Pivot Table** (17MB XLSX, manual download from dfat.gov.au) → `data/raw/australia/`
  - Sheet "Pivot": 265 SITC commodity rows × 50 monthly columns (Jan 2022–Feb 2026)
  - Values: AUD thousands, trade recorded basis
  - Header at row 15 (0-indexed), data starts row 16
  - Key finding: Gold (SITC 971) is Australia's 3rd largest export commodity (A$144B in 2024+)
- **ABS bilateral data**: Not available via direct API download; DFAT pivot table covers total Australian trade by commodity

---

## Task 4: Standardize

**Dates**: All → `YYYY-MM-DD`, column = `date`. Filter to 2024-01-01+.
**Countries**: ISO 3166 alpha-3 mapping table → `data/reference/country_mapping.csv`
**Missing values**: FRED "." → NaN via `pd.to_numeric(errors="coerce")`
**Currency**: Note AUD vs USD in column names. DFAT/ABS = AUD thousands. FRED = USD.

---

## Task 5: Execute 8 Joins

### Join 1 — Act I: Tariff Rate × Market Reaction (Daily)
**Output**: `data/joined/viz1_tariff_market_fear.csv`
- Merge: Yale tariff rate + S&P 500 + VIX on `date`
- Add event annotations from `data/reference/key_events.csv`
- **Story**: "Every announcement spiked fear and crashed markets"

### Join 2 — Act II: Tariff × CPI × Consumer Sentiment (Monthly)
**Output**: `data/joined/viz2_price_pass_through.csv`
- Merge monthly tariff rate + CPI + Michigan Sentiment on `month`
- **Story**: "Prices rose, confidence fell — but WHO paid more?"

### Join 3 — Act II: Distributional Burden (Income Quintiles)
**Output**: `data/joined/viz3_who_pays.csv`
- Manual table from TPC + Yale distributional data
- Columns: income_quintile, avg_tax_increase_usd, fed_tax_rate_increase_pp, share_of_income_lost_pct
- **Story**: "Bottom 10% loses 1.14% of income. Top 10% loses 0.36%. Same policy, different pain — a 3.2x gap." (Yale Budget Lab Feb 2026; decile-level, not quintile.)
- **THIS IS THE CENTRAL VISUALIZATION**
- **Note**: The Python snippet below shows the *original quintile-level draft* from an earlier revision. The shipping dataset is `data/joined/viz3_who_pays.csv` (decile-level, 20 rows across 2 scenarios), produced by `scripts/14_rebuild_data.py`.

```python
import pandas as pd
viz3 = pd.DataFrame({
    "income_group": ["Bottom 20%", "Second 20%", "Middle 20%", "Fourth 20%", "Top 20%", "Top 1%"],
    "avg_tax_increase_usd": [400, 960, 1610, 2770, 7330, 39800],
    "fed_tax_rate_increase_pp": [1.9, 1.8, 1.6, 1.4, 1.3, 0.7],
    "share_of_income_lost_pct": [3.6, 2.8, 2.0, 1.6, 1.2, 1.1],
    "most_affected_goods": ["Apparel, shoes, food", "Clothing, household basics", "Electronics, furniture", "Vehicles, appliances", "Vehicles, luxury goods", "Financial assets, minimal goods impact"],
    "source": ["TPC/Yale", "TPC/Yale", "TPC/Yale", "TPC/Yale", "TPC/Yale", "TPC/Yale"],
})
viz3.to_csv("data/joined/viz3_who_pays.csv", index=False)
```

### Join 4 — Act III: Trade Deficit Paradox (Monthly)
**Output**: `data/joined/viz4_deficit_paradox.csv`
- Merge trade balance + imports + tariff rate on `month`
- **Story**: "Tariffs were supposed to shrink the deficit. They didn't."

### Join 5 — Act III: Manufacturing Trade-off (Monthly)
**Output**: `data/joined/viz5_manufacturing_tradeoff.csv`
- Merge industrial production + unemployment + tariff rate on `month`
- Add annotation: "Investment announcements surging BUT 83K jobs lost in 2025"
- **Story**: "Factories were promised. Investment rose. But the jobs didn't follow — yet."

### Join 6 — Act III: Global Map (Country Level)
**Output**: `data/joined/viz6_world_map.csv`
- Merge country tariff rates + trade flow changes on `iso3`
- Include Australia gold export data point as callout
- **Story**: "Trade is rerouting around America. Allies are seeking alternatives."

### Join 7 — Act IV: What-If Scenarios
**Output**: `data/joined/viz7_whatif.csv`
- Parameters from Yale Budget Lab reports

```python
viz7 = pd.DataFrame({
    "scenario": [
        "Let S122 expire (Jul 24)",
        "Congress extends S122 at 10%",
        "Congress extends S122 at 15%",
        "Replace with targeted S232/S301",
        "Restore IEEPA-level rates (if new authority)",
    ],
    "eff_tariff_rate": [8.1, 10.5, 13.0, 12.0, 16.8],
    "gdp_impact_pct": [-0.1, -0.2, -0.3, -0.25, -0.4],
    "unemployment_increase_pp": [0.1, 0.2, 0.4, 0.3, 0.7],
    "price_increase_pct": [0.3, 0.4, 0.6, 0.5, 1.2],
    "household_cost_bottom20_usd": [150, 250, 400, 300, 700],
    "household_cost_top20_usd": [3000, 4500, 7330, 5500, 12000],
    "tariff_revenue_10yr_trillion": [1.2, 1.5, 2.0, 1.8, 2.5],
    "source": ["Yale/TPC", "Yale/TPC", "Yale/TPC", "Yale/TPC est.", "Yale Nov 2025"],
})
viz7.to_csv("data/joined/viz7_whatif.csv", index=False)
```

### Join 8 — Act IV: Recession Signal (Daily)
**Output**: `data/joined/viz8_recession_signal.csv`
- Merge 10Y Treasury + 2Y-10Y spread + VIX on `date`
- **Story**: "Financial markets are sending a warning. The yield curve is watching."

---

## Key Events Timeline

Create `data/reference/key_events.csv` with ~27 events. Include columns:
- `date` (YYYY-MM-DD)
- `event_short` (< 60 chars)
- `event_detail` (full description)
- `impact_type` (tariff_up / tariff_down / retaliation / legal / negotiation / threat)
- `eff_tariff_rate_approx` (approximate rate at that point)
- `story_act` (I / II / III / IV)

Key events to include:
- Jan 20, 2025: Inauguration
- Feb 1: IEEPA tariffs announced
- Feb 4: China retaliates
- Mar 19: Powell says "transitory"
- Apr 2: Liberation Day
- Apr 4: Powell walks back "transitory"
- Apr 10: US-China 125% peak
- May 14: Geneva talks — mutual reduction
- Aug 22: Powell Jackson Hole — "one-time price level shift"
- Aug 25: Federal Circuit rules against IEEPA
- Oct 30: US-China Busan — tariffs reduced
- Dec 10: Powell "very unusual economy"; 3rd rate cut
- Feb 20, 2026: SCOTUS 6-3 strikes down IEEPA
- Feb 24: S122 takes effect
- Mar 11: S301 investigations launched
- Jul 24: S122 expires (FUTURE — key deadline)

---

## Visualization Plan (8+ visuals)

| # | Visual | Type | Act | Emotional Point |
|---|--------|------|-----|-----------------|
| 1 | Effective tariff rate timeline + events | Line + annotations | I | "Century-high in 3 months" |
| 2 | S&P 500 + VIX on tariff announcement days | Dual-axis + events | I | "Every announcement = panic" |
| 3 | **Income decile burden comparison** | **Horizontal bar + scenario toggle** | **II** | **"3.2x more for the poorest" — CENTRAL** |
| 4 | CPI by category (apparel +37%, shoes +39%) | Horizontal bar | II | "The poor buy more of what got taxed most" |
| 5 | Trade deficit vs tariff rate | Dual-axis line | III | "The paradox" |
| 6 | Manufacturing: investment vs jobs | Dual-axis | III | "Honest trade-off" |
| 7 | World map: tariff rates + trade rerouting | Choropleth | III | "Trade routes are shifting" |
| 8 | What-If slider: tariff rate → burden by income | Interactive | IV | "Your choice, Mr. President" |
| 9 | Yield curve + recession probability | Area chart | IV | "The clock is ticking" |

### Advanced Features (3 required)

1. **What-If Parameterization**: Slider adjusts tariff rate → real-time update of GDP, jobs, prices, AND distributional burden by income quintile
2. **Context-Aware Filtering**: Click a timeline event → all other charts update to show that moment's data
3. **Narrative Scrollytelling**: Four-act scroll structure: Scale → Who Pays → What It Bought → The Choice

---

## Validation Checklist

```python
expected = {
    "data/joined/viz1_tariff_market_fear.csv": ["date","sp500"],
    "data/joined/viz2_price_pass_through.csv": ["date","cpi"],
    "data/joined/viz3_who_pays.csv": ["income_group","share_of_income_lost_pct"],
    "data/joined/viz4_deficit_paradox.csv": ["date"],
    "data/joined/viz5_manufacturing_tradeoff.csv": ["date"],
    "data/joined/viz6_world_map.csv": ["iso3"],
    "data/joined/viz7_whatif.csv": ["scenario","eff_tariff_rate"],
    "data/joined/viz8_recession_signal.csv": ["date"],
    "data/reference/key_events.csv": ["date","event_short","story_act"],
    "data/reference/country_mapping.csv": ["name_variant","iso3"],
}
```

---

## Critical Notes

1. **Never modify raw files.** `data/raw/` is read-only.
2. **FRED "." = NaN.** Use `pd.to_numeric(errors="coerce")`.
3. **DFAT/ABS XLSX**: Explore with `header=None, nrows=20` first. Complex multi-level headers. Header at row 15, data at row 16.
4. **Print shape + date range at every step.**
5. **viz3_who_pays.csv is the most important output.** The distributional data is the emotional and argumentative core of the entire project.
6. **Daily tariff rate**: viz1 uses real import-weighted data from tradewartracker (Jan–Jun 2025, 176 days) + key_events step function for the rest of the timeline.
7. **Honesty in Act III**: Include manufacturing investment data alongside job loss data. The story is a trade-off, not a simple failure.
8. **FRED Gold delisted**: LBMA Gold was removed from FRED on Jan 31, 2022. Use datasets/gold-prices (GitHub) monthly data instead.
9. **GTA login-walled**: GTA data center requires registration. Use Kratosfury/Tariffs-USA (57 countries), White House gist (126 countries), and tradewartracker repo as alternatives.
10. **Run the app**: `conda activate dvn-at3 && cd tariff-story && streamlit run app/app.py`
