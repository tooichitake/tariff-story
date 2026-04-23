"""
Phase 3: Create all 8 joined datasets for visualization.
viz3 and viz7 already created (hardcoded). This creates viz1,2,4,5,6,8.
"""
import pandas as pd
import numpy as np
import os

from pathlib import Path
BASE = str(Path(__file__).resolve().parent.parent)
CLEANED = os.path.join(BASE, "data", "cleaned")
JOINED = os.path.join(BASE, "data", "joined")
REF = os.path.join(BASE, "data", "reference")


def load_fred(name):
    path = os.path.join(CLEANED, f"fred_{name}.csv")
    if os.path.exists(path):
        df = pd.read_csv(path, parse_dates=["date"])
        return df
    return None


# Load key events for annotations
key_events = pd.read_csv(os.path.join(REF, "key_events.csv"), parse_dates=["date"])

# ============================================================
# Build a daily effective tariff rate from key_events
# (step function: rate holds until next event)
# ============================================================
print("=== Building daily tariff rate from key events ===")
tariff_events = key_events[["date", "eff_tariff_rate_approx"]].dropna().sort_values("date")
date_range = pd.date_range("2024-01-01", "2026-07-24", freq="D")
tariff_daily = pd.DataFrame({"date": date_range})

# Before first event (Jan 20, 2025), rate was ~2.5%
tariff_daily["eff_tariff_rate"] = 2.5
for _, row in tariff_events.iterrows():
    tariff_daily.loc[tariff_daily["date"] >= row["date"], "eff_tariff_rate"] = row["eff_tariff_rate_approx"]

print(f"  Daily tariff rate: {tariff_daily.shape[0]} rows")
print(f"  Range: {tariff_daily['eff_tariff_rate'].min():.1f}% to {tariff_daily['eff_tariff_rate'].max():.1f}%")

# ============================================================
# viz1: Tariff Rate x Market Reaction (Daily)
# ============================================================
print("\n=== viz1_tariff_market_fear.csv ===")
sp500 = load_fred("sp500")
vix = load_fred("vix")

if sp500 is not None and vix is not None:
    viz1 = tariff_daily.merge(sp500, on="date", how="left")
    viz1 = viz1.merge(vix, on="date", how="left")

    # Add event flags
    viz1 = viz1.merge(
        key_events[["date", "event_short", "impact_type", "story_act"]],
        on="date", how="left"
    )
    viz1["is_event"] = viz1["event_short"].notna()

    viz1.to_csv(os.path.join(JOINED, "viz1_tariff_market_fear.csv"), index=False)
    print(f"  Shape: {viz1.shape}")
    print(f"  Date range: {viz1['date'].min().date()} to {viz1['date'].max().date()}")
    print(f"  SP500 non-null: {viz1['sp500'].notna().sum()}, VIX non-null: {viz1['vix'].notna().sum()}")
    print(f"  Events flagged: {viz1['is_event'].sum()}")

# ============================================================
# viz2: Tariff x CPI x Consumer Sentiment (Monthly)
# ============================================================
print("\n=== viz2_price_pass_through.csv ===")
cpi = load_fred("cpi")

if cpi is not None:
    # Create monthly tariff rate
    tariff_monthly = tariff_daily.copy()
    tariff_monthly["month"] = tariff_monthly["date"].dt.to_period("M")
    tariff_monthly = tariff_monthly.groupby("month")["eff_tariff_rate"].last().reset_index()
    tariff_monthly["date"] = tariff_monthly["month"].dt.to_timestamp()
    tariff_monthly.drop(columns=["month"], inplace=True)

    cpi["date"] = pd.to_datetime(cpi["date"])
    viz2 = tariff_monthly.merge(cpi, on="date", how="inner")

    # Add CPI % change
    viz2["cpi_pct_change"] = viz2["cpi"].pct_change() * 100

    # Load commodity prices from Yale for category breakdown
    commodity_path = os.path.join(CLEANED, "yale_commodity_prices.csv")
    if os.path.exists(commodity_path):
        commodity = pd.read_csv(commodity_path)
        print(f"  Yale commodity prices available: {commodity.shape}")

    viz2.to_csv(os.path.join(JOINED, "viz2_price_pass_through.csv"), index=False)
    print(f"  Shape: {viz2.shape}")
    print(f"  Date range: {viz2['date'].min().date()} to {viz2['date'].max().date()}")

# ============================================================
# viz4: Trade Deficit Paradox (Monthly)
# ============================================================
print("\n=== viz4_deficit_paradox.csv ===")
trade_balance = load_fred("trade_balance")

if trade_balance is not None:
    tariff_monthly2 = tariff_daily.copy()
    tariff_monthly2["month"] = tariff_monthly2["date"].dt.to_period("M")
    tariff_monthly2 = tariff_monthly2.groupby("month")["eff_tariff_rate"].last().reset_index()
    tariff_monthly2["date"] = tariff_monthly2["month"].dt.to_timestamp()
    tariff_monthly2.drop(columns=["month"], inplace=True)

    trade_balance["date"] = pd.to_datetime(trade_balance["date"])
    viz4 = tariff_monthly2.merge(trade_balance, on="date", how="inner")

    viz4.to_csv(os.path.join(JOINED, "viz4_deficit_paradox.csv"), index=False)
    print(f"  Shape: {viz4.shape}")
    print(f"  Trade balance range: {viz4['trade_balance'].min():.1f} to {viz4['trade_balance'].max():.1f}")

# ============================================================
# viz5: Manufacturing Trade-off (Monthly)
# ============================================================
print("\n=== viz5_manufacturing_tradeoff.csv ===")
industrial = load_fred("industrial_prod")
unemployment = load_fred("unemployment")
mfg_employment = load_fred("mfg_employment")
mfg_job_openings = load_fred("mfg_job_openings")

if industrial is not None and unemployment is not None:
    tariff_monthly3 = tariff_daily.copy()
    tariff_monthly3["month"] = tariff_monthly3["date"].dt.to_period("M")
    tariff_monthly3 = tariff_monthly3.groupby("month")["eff_tariff_rate"].last().reset_index()
    tariff_monthly3["date"] = tariff_monthly3["month"].dt.to_timestamp()
    tariff_monthly3.drop(columns=["month"], inplace=True)

    industrial["date"] = pd.to_datetime(industrial["date"])
    unemployment["date"] = pd.to_datetime(unemployment["date"])

    viz5 = tariff_monthly3.merge(industrial, on="date", how="inner")
    viz5 = viz5.merge(unemployment, on="date", how="inner")

    # Add manufacturing employment (thousands of persons)
    if mfg_employment is not None:
        mfg_employment["date"] = pd.to_datetime(mfg_employment["date"])
        viz5 = viz5.merge(mfg_employment, on="date", how="left")
        print(f"  Added mfg_employment: {mfg_employment.shape[0]} rows")

    # Add manufacturing job openings (thousands)
    if mfg_job_openings is not None:
        mfg_job_openings["date"] = pd.to_datetime(mfg_job_openings["date"])
        viz5 = viz5.merge(mfg_job_openings, on="date", how="left")
        print(f"  Added mfg_job_openings: {mfg_job_openings.shape[0]} rows")

    viz5.to_csv(os.path.join(JOINED, "viz5_manufacturing_tradeoff.csv"), index=False)
    print(f"  Shape: {viz5.shape}")

# ============================================================
# viz6: World Map (Country Level)
# ============================================================
print("\n=== viz6_world_map.csv ===")
tariffs_path = os.path.join(CLEANED, "kaggle_trump_tariffs_by_country.csv")
calc_path = os.path.join(CLEANED, "kaggle_tariff_calculations_plus_population.csv")

if os.path.exists(tariffs_path):
    tariffs = pd.read_csv(tariffs_path)
    print(f"  Trump tariffs: {tariffs.shape}")

    # Clean tariff percentages
    for col in ["tariffs_charged_to_usa", "reciprocal_tariffs"]:
        if col in tariffs.columns:
            tariffs[col] = pd.to_numeric(tariffs[col], errors="coerce") * 100  # Convert from decimal

    # Load Yale regional tariffs if available
    yale_reg_path = os.path.join(CLEANED, "yale_regional_tariffs.csv")
    if os.path.exists(yale_reg_path):
        yale_reg = pd.read_csv(yale_reg_path)
        print(f"  Yale regional tariffs: {yale_reg.shape}")

    # Use tariffs as base for viz6
    viz6 = tariffs.copy()
    if "iso3" not in viz6.columns:
        country_map = pd.read_csv(os.path.join(REF, "country_mapping.csv"))
        name_to_iso3 = dict(zip(country_map["name_variant"], country_map["iso3"]))
        viz6["iso3"] = viz6["country"].map(name_to_iso3)

    viz6 = viz6.dropna(subset=["iso3"])
    viz6.to_csv(os.path.join(JOINED, "viz6_world_map.csv"), index=False)
    print(f"  Shape: {viz6.shape}")
    print(f"  Countries with ISO3: {viz6['iso3'].nunique()}")

# ============================================================
# viz8: Recession Signal (Daily)
# ============================================================
print("\n=== viz8_recession_signal.csv ===")
treasury = load_fred("treasury_10y")
yield_spread = load_fred("yield_spread")
vix2 = load_fred("vix")

if treasury is not None and yield_spread is not None:
    viz8 = treasury.merge(yield_spread, on="date", how="inner")
    if vix2 is not None:
        viz8 = viz8.merge(vix2, on="date", how="left")

    # Derive recession signal
    viz8["yield_inverted"] = viz8["yield_spread"] < 0
    viz8["recession_warning"] = viz8["yield_spread"].rolling(30).mean() < 0

    viz8.to_csv(os.path.join(JOINED, "viz8_recession_signal.csv"), index=False)
    print(f"  Shape: {viz8.shape}")
    print(f"  Inverted days: {viz8['yield_inverted'].sum()}")

# ============================================================
# Validation
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

all_pass = True
for fname, required_cols in expected.items():
    fpath = os.path.join(JOINED, fname)
    if os.path.exists(fpath):
        df = pd.read_csv(fpath)
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            print(f"  FAIL {fname}: missing columns {missing}")
            all_pass = False
        else:
            print(f"  PASS {fname}: {df.shape}")
    else:
        print(f"  FAIL {fname}: file not found")
        all_pass = False

# Also check reference files
ref_expected = {
    "key_events.csv": ["date", "event_short", "story_act"],
    "country_mapping.csv": ["name_variant", "iso3"],
}
for fname, required_cols in ref_expected.items():
    fpath = os.path.join(REF, fname)
    if os.path.exists(fpath):
        df = pd.read_csv(fpath)
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            print(f"  FAIL ref/{fname}: missing columns {missing}")
            all_pass = False
        else:
            print(f"  PASS ref/{fname}: {df.shape}")

if all_pass:
    print("\n=== ALL 10 OUTPUT FILES VALIDATED ===")
else:
    print("\n=== SOME FILES FAILED VALIDATION ===")
