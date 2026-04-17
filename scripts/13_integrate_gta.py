"""
Integrate GTA alternative data into cleaned files and update joined datasets.
Key improvements:
1. daily_tariff.csv replaces our step-function tariff rate (more accurate)
2. gta_tariffs_usa.xlsx + whitehouse tariffs enrich viz6 world map
"""
import pandas as pd
import numpy as np
import os
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from pathlib import Path
BASE = str(Path(__file__).resolve().parent.parent)
RAW_OTHER = os.path.join(BASE, "data", "raw", "other")
CLEANED = os.path.join(BASE, "data", "cleaned")
JOINED = os.path.join(BASE, "data", "joined")
REF = os.path.join(BASE, "data", "reference")

# ============================================================
# 1. Clean daily tariff rate (tradewartracker)
# ============================================================
print("=== Daily Tariff Rate ===")
daily = pd.read_csv(os.path.join(RAW_OTHER, "tradewar_daily_tariff.csv"))
daily = daily[["date", "import_weighted_avg_tariff"]].copy()
daily["date"] = pd.to_datetime(daily["date"])
daily.rename(columns={"import_weighted_avg_tariff": "eff_tariff_rate"}, inplace=True)
daily.to_csv(os.path.join(CLEANED, "daily_tariff_rate.csv"), index=False)
print(f"  Shape: {daily.shape}")
print(f"  Range: {daily['date'].min().date()} to {daily['date'].max().date()}")
print(f"  Tariff: {daily['eff_tariff_rate'].min():.2f}% to {daily['eff_tariff_rate'].max():.2f}%")

# ============================================================
# 2. Clean GTA tariffs XLSX (country level)
# ============================================================
print("\n=== GTA Tariffs by Country ===")
gta = pd.read_excel(
    os.path.join(RAW_OTHER, "gta_tariffs_usa.xlsx"),
    sheet_name="Tariff List", header=None
)
# Header at row 3
gta.columns = gta.iloc[3].tolist()
gta = gta.iloc[5:].copy()  # data starts at row 5
gta = gta.dropna(subset=["Country"])

# Clean column names
gta.columns = [str(c).strip().replace('\n', ' ') for c in gta.columns]
rename_map = {}
for c in gta.columns:
    cl = c.lower()
    if 'country' in cl: rename_map[c] = 'country'
    elif 'export' in cl: rename_map[c] = 'exports_bn'
    elif 'import' in cl: rename_map[c] = 'imports_bn'
    elif 'deficit' in cl: rename_map[c] = 'trade_deficit_bn'
    elif 'reciprocal tariff by' in cl: rename_map[c] = 'reciprocal_tariff'
gta.rename(columns=rename_map, inplace=True)

# Add ISO3 mapping
country_map = pd.read_csv(os.path.join(REF, "country_mapping.csv"))
name_to_iso3 = dict(zip(country_map["name_variant"], country_map["iso3"]))
gta["iso3"] = gta["country"].str.strip().str.rstrip("*").str.strip().map(name_to_iso3)

# Convert numeric columns
for col in ["exports_bn", "imports_bn", "trade_deficit_bn", "reciprocal_tariff"]:
    if col in gta.columns:
        gta[col] = pd.to_numeric(gta[col], errors="coerce")

gta_clean = gta[["country", "iso3", "exports_bn", "imports_bn", "trade_deficit_bn", "reciprocal_tariff"]].dropna(subset=["country"])
gta_clean.to_csv(os.path.join(CLEANED, "gta_tariffs_by_country.csv"), index=False)
print(f"  Shape: {gta_clean.shape}")
print(f"  ISO3 mapped: {gta_clean['iso3'].notna().sum()}/{len(gta_clean)}")
print(gta_clean.head(5).to_string(index=False))

# ============================================================
# 3. Clean Whitehouse tariffs (Liberation Day)
# ============================================================
print("\n=== Whitehouse Liberation Day Tariffs ===")
wh = pd.read_csv(os.path.join(RAW_OTHER, "whitehouse_trump_tariffs_20250402.csv"))
wh.columns = ["country", "tariffs_charged_to_usa", "us_reciprocal_tariffs"]

# Clean percentage strings
for col in ["tariffs_charged_to_usa", "us_reciprocal_tariffs"]:
    wh[col] = wh[col].astype(str).str.replace("%", "").str.strip()
    wh[col] = pd.to_numeric(wh[col], errors="coerce") / 100  # to decimal

wh["iso3"] = wh["country"].str.strip().map(name_to_iso3)
wh.to_csv(os.path.join(CLEANED, "whitehouse_tariffs_20250402.csv"), index=False)
print(f"  Shape: {wh.shape}")
print(f"  ISO3 mapped: {wh['iso3'].notna().sum()}/{len(wh)}")

# ============================================================
# 4. Update viz1 with real daily tariff data
# ============================================================
print("\n=== Updating viz1_tariff_market_fear.csv ===")
key_events = pd.read_csv(os.path.join(REF, "key_events.csv"), parse_dates=["date"])
sp500 = pd.read_csv(os.path.join(CLEANED, "fred_sp500.csv"), parse_dates=["date"])
vix = pd.read_csv(os.path.join(CLEANED, "fred_vix.csv"), parse_dates=["date"])

# Build combined tariff rate: real data where available, step function elsewhere
date_range = pd.date_range("2024-01-01", "2026-07-24", freq="D")
tariff_full = pd.DataFrame({"date": date_range})

# Start with step function from key_events
tariff_events = key_events[["date", "eff_tariff_rate_approx"]].dropna().sort_values("date")
tariff_full["eff_tariff_rate"] = 2.5
for _, row in tariff_events.iterrows():
    tariff_full.loc[tariff_full["date"] >= row["date"], "eff_tariff_rate"] = row["eff_tariff_rate_approx"]

# Override with real daily data where available
daily["date"] = pd.to_datetime(daily["date"])
for _, row in daily.iterrows():
    mask = tariff_full["date"] == row["date"]
    if mask.any():
        tariff_full.loc[mask, "eff_tariff_rate"] = row["eff_tariff_rate"]

# Add source indicator
tariff_full["tariff_source"] = "key_events_step"
for _, row in daily.iterrows():
    mask = tariff_full["date"] == row["date"]
    if mask.any():
        tariff_full.loc[mask, "tariff_source"] = "tradewartracker_daily"

viz1 = tariff_full.merge(sp500, on="date", how="left")
viz1 = viz1.merge(vix, on="date", how="left")
viz1 = viz1.merge(
    key_events[["date", "event_short", "impact_type", "story_act"]],
    on="date", how="left"
)
viz1["is_event"] = viz1["event_short"].notna()

viz1.to_csv(os.path.join(JOINED, "viz1_tariff_market_fear.csv"), index=False)
print(f"  Shape: {viz1.shape}")
real_data_days = (viz1["tariff_source"] == "tradewartracker_daily").sum()
print(f"  Real daily tariff data: {real_data_days} days")
print(f"  Step function fallback: {len(viz1) - real_data_days} days")

# ============================================================
# 5. Update viz6 with GTA + Whitehouse data
# ============================================================
print("\n=== Updating viz6_world_map.csv ===")

# Start with Kaggle data
kaggle = pd.read_csv(os.path.join(CLEANED, "kaggle_trump_tariffs_by_country.csv"))
print(f"  Kaggle base: {kaggle.shape}")

# Merge GTA data
if "iso3" in kaggle.columns and "iso3" in gta_clean.columns:
    viz6 = kaggle.merge(
        gta_clean[["iso3", "exports_bn", "imports_bn", "trade_deficit_bn", "reciprocal_tariff"]],
        on="iso3", how="outer", suffixes=("_kaggle", "_gta")
    )
else:
    viz6 = kaggle.copy()

# Also merge Whitehouse data
if "iso3" in viz6.columns and "iso3" in wh.columns:
    viz6 = viz6.merge(
        wh[["iso3", "tariffs_charged_to_usa", "us_reciprocal_tariffs"]],
        on="iso3", how="outer", suffixes=("", "_wh")
    )

# Create a unified tariff column (prefer GTA > Whitehouse > Kaggle)
if "reciprocal_tariff" in viz6.columns:
    viz6["tariff_rate_final"] = viz6["reciprocal_tariff"]
if "us_reciprocal_tariffs" in viz6.columns:
    viz6["tariff_rate_final"] = viz6["tariff_rate_final"].fillna(viz6["us_reciprocal_tariffs"])
if "reciprocal_tariffs" in viz6.columns:
    viz6["tariff_rate_final"] = viz6["tariff_rate_final"].fillna(viz6["reciprocal_tariffs"])

viz6 = viz6.dropna(subset=["iso3"])
viz6.to_csv(os.path.join(JOINED, "viz6_world_map.csv"), index=False)
print(f"  Updated viz6: {viz6.shape}")
print(f"  Countries: {viz6['iso3'].nunique()}")

# ============================================================
# 6. Re-validate all files
# ============================================================
print("\n=== VALIDATION ===")
expected = {
    "viz1_tariff_market_fear.csv": ["date", "sp500"],
    "viz2_price_pass_through.csv": ["date", "cpi"],
    "viz3_who_pays.csv": ["income_group", "share_of_income_lost_pct"],
    "viz4_deficit_paradox.csv": ["date"],
    "viz5_manufacturing_tradeoff.csv": ["date"],
    "viz6_world_map.csv": ["iso3"],
    "viz7_whatif.csv": ["scenario", "eff_tariff_rate"],
    "viz8_recession_signal.csv": ["date"],
}
for fname, cols in expected.items():
    path = os.path.join(JOINED, fname)
    df = pd.read_csv(path)
    missing = [c for c in cols if c not in df.columns]
    status = "PASS" if not missing else f"FAIL (missing {missing})"
    print(f"  {status} {fname}: {df.shape}")

print("\n=== DONE ===")
