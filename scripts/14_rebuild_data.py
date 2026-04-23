"""
Phase 14: Rebuild all visualization datasets for the enhanced narrative.
Tasks:
  1. Parse Yale distributional raw -> 10 decile x 2 scenario viz3
  2. Clean consumer sentiment -> cleaned + merge into viz2
  3. Process country-by-time -> enhanced viz6 with temporal dimension
  4. Merge Fed Funds into viz8
  5. Process customs duties -> cleaned
  6. Validate all outputs
"""
import pandas as pd
import numpy as np
import os
import shutil

from pathlib import Path
BASE = str(Path(__file__).resolve().parent.parent)
RAW_FRED = os.path.join(BASE, "data", "raw", "fred")
RAW_OTHER = os.path.join(BASE, "data", "raw", "other")
CLEANED = os.path.join(BASE, "data", "cleaned")
JOINED = os.path.join(BASE, "data", "joined")
REF = os.path.join(BASE, "data", "reference")

for d in [CLEANED, JOINED, REF]:
    os.makedirs(d, exist_ok=True)


def save_joined(df, filename):
    df.to_csv(os.path.join(JOINED, filename), index=False)
    print(f"  Saved: {filename} ({df.shape[0]} rows, {df.shape[1]} cols)")


def save_cleaned(df, filename):
    df.to_csv(os.path.join(CLEANED, filename), index=False)
    print(f"  Saved: {filename} ({df.shape[0]} rows)")


# ============================================================
# TASK 1: Parse Yale distributional raw -> enhanced viz3
# ============================================================
print("=" * 60)
print("TASK 1: Yale 10-decile distributional data")
print("=" * 60)

yale_raw_path = os.path.join(CLEANED, "yale_distributional_raw.csv")
df_raw = pd.read_csv(yale_raw_path, header=None)

# Row 11 (0-indexed 10): Current Policy - % of income
# Row 12 (0-indexed 11): Current Policy - USD
# Row 15 (0-indexed 14): IEEPA Upheld - % of income
# Row 16 (0-indexed 15): IEEPA Upheld - USD
current_pct = df_raw.iloc[10, 1:11].astype(float).values
current_usd = df_raw.iloc[11, 1:11].astype(float).values
ieepa_pct = df_raw.iloc[14, 1:11].astype(float).values
ieepa_usd = df_raw.iloc[15, 1:11].astype(float).values

decile_labels = [f"Decile {i}" for i in range(1, 11)]

# Most affected goods by decile (low income = essentials, high income = luxury)
goods_map = {
    "Decile 1": "Apparel, shoes, food",
    "Decile 2": "Apparel, shoes, food",
    "Decile 3": "Clothing, household basics",
    "Decile 4": "Clothing, household basics",
    "Decile 5": "Electronics, furniture",
    "Decile 6": "Electronics, furniture",
    "Decile 7": "Electronics, appliances",
    "Decile 8": "Vehicles, appliances",
    "Decile 9": "Vehicles, luxury goods",
    "Decile 10": "Vehicles, financial assets",
}

rows = []
for i, label in enumerate(decile_labels):
    rows.append({
        "decile": i + 1,
        "decile_label": label,
        "scenario": "Current Policy (S122)",
        "pct_income_lost": round(abs(current_pct[i]), 4),
        "usd_cost": round(abs(current_usd[i]), 2),
        "most_affected_goods": goods_map[label],
    })
    rows.append({
        "decile": i + 1,
        "decile_label": label,
        "scenario": "IEEPA Upheld",
        "pct_income_lost": round(abs(ieepa_pct[i]), 4),
        "usd_cost": round(abs(ieepa_usd[i]), 2),
        "most_affected_goods": goods_map[label],
    })

viz3 = pd.DataFrame(rows)
save_joined(viz3, "viz3_who_pays.csv")

# Quick validation
current = viz3[viz3["scenario"] == "Current Policy (S122)"]
print(f"  Decile 1 pct: {current.iloc[0]['pct_income_lost']:.4f}")
print(f"  Decile 10 pct: {current.iloc[9]['pct_income_lost']:.4f}")
print(f"  Ratio: {current.iloc[0]['pct_income_lost'] / current.iloc[9]['pct_income_lost']:.1f}x")

# ============================================================
# TASK 2: Consumer sentiment -> cleaned + merge into viz2
# ============================================================
print("\n" + "=" * 60)
print("TASK 2: Consumer Sentiment (UMCSENT)")
print("=" * 60)

sent_path = os.path.join(RAW_FRED, "consumer_sentiment.csv")
sent = pd.read_csv(sent_path)
sent.columns = ["date", "consumer_sentiment"]
sent["date"] = pd.to_datetime(sent["date"])
sent = sent[sent["date"] >= "2024-01-01"].copy()
sent["consumer_sentiment"] = pd.to_numeric(sent["consumer_sentiment"], errors="coerce")
sent = sent.dropna()
save_cleaned(sent, "fred_consumer_sentiment.csv")

# Merge into viz2
viz2_path = os.path.join(JOINED, "viz2_price_pass_through.csv")
viz2 = pd.read_csv(viz2_path, parse_dates=["date"])
viz2 = viz2.merge(sent, on="date", how="left")
save_joined(viz2, "viz2_price_pass_through.csv")
print(f"  Sentiment range: {sent['consumer_sentiment'].min():.1f} - {sent['consumer_sentiment'].max():.1f}")

# ============================================================
# TASK 3: Country-by-time -> enhanced viz6
# ============================================================
print("\n" + "=" * 60)
print("TASK 3: Country-by-time tariff data for animated map")
print("=" * 60)

cbt_path = os.path.join(RAW_OTHER, "tradewar_country-by-time.csv")
cbt = pd.read_csv(cbt_path)
cbt["date"] = pd.to_datetime(cbt["date"])
cbt.rename(columns={"effective tariff": "effective_tariff", "total imports": "total_imports", "2024 tariff": "tariff_2024"}, inplace=True)

print(f"  Raw: {cbt.shape[0]} rows, {cbt['country_name'].nunique()} countries, {cbt['date'].nunique()} dates")

# Country name to ISO3 mapping
country_map_path = os.path.join(REF, "country_mapping.csv")
country_map = pd.read_csv(country_map_path)
name_to_iso3 = dict(zip(country_map["name_variant"], country_map["iso3"]))

# Add common missing mappings (all 51 countries in tradewar_country-by-time.csv)
extra_mappings = {
    "CHINA": "CHN", "MEXICO": "MEX", "CANADA": "CAN", "JAPAN": "JPN",
    "KOREA, SOUTH": "KOR", "VIETNAM": "VNM", "TAIWAN": "TWN", "INDIA": "IND",
    "UNITED KINGDOM": "GBR", "SWITZERLAND": "CHE", "MALAYSIA": "MYS",
    "THAILAND": "THA", "BRAZIL": "BRA", "SINGAPORE": "SGP", "INDONESIA": "IDN",
    "AUSTRALIA": "AUS", "GERMANY": "DEU", "FRANCE": "FRA", "ITALY": "ITA",
    "NETHERLANDS": "NLD", "IRELAND": "IRL", "ISRAEL": "ISR", "SOUTH AFRICA": "ZAF",
    "COLOMBIA": "COL", "CHILE": "CHL", "SAUDI ARABIA": "SAU", "BANGLADESH": "BGD",
    "CAMBODIA": "KHM", "PAKISTAN": "PAK", "COSTA RICA": "CRI",
    # Previously missing mappings
    "ALGERIA": "DZA", "ANGOLA": "AGO", "ARGENTINA": "ARG",
    "DOMINICAN REPUBLIC": "DOM", "ECUADOR": "ECU", "EGYPT": "EGY",
    "EL SALVADOR": "SLV", "EUROPEAN UNION": "EUU",
    "GUATEMALA": "GTM", "HONDURAS": "HND", "HONG KONG": "HKG",
    "IRAQ": "IRQ", "KUWAIT": "KWT", "NEW ZEALAND": "NZL",
    "NICARAGUA": "NIC", "NIGERIA": "NGA", "NORWAY": "NOR",
    "PERU": "PER", "PHILIPPINES": "PHL", "RUSSIA": "RUS",
    "SLOVAKIA": "SVK", "SRI LANKA": "LKA",
    "TRINIDAD AND TOBAGO": "TTO", "TURKEY": "TUR",
    "UNITED ARAB EMIRATES": "ARE", "VENEZUELA": "VEN",
}
name_to_iso3.update(extra_mappings)

cbt["iso3"] = cbt["country_name"].map(name_to_iso3)

# Expand EU data to individual member states
# The US applies tariffs to the EU as a bloc, so all members share the same rate
eu_members = {
    "Austria": "AUT", "Belgium": "BEL", "Bulgaria": "BGR", "Croatia": "HRV",
    "Cyprus": "CYP", "Czech Republic": "CZE", "Denmark": "DNK", "Estonia": "EST",
    "Finland": "FIN", "France": "FRA", "Germany": "DEU", "Greece": "GRC",
    "Hungary": "HUN", "Ireland": "IRL", "Italy": "ITA", "Latvia": "LVA",
    "Lithuania": "LTU", "Luxembourg": "LUX", "Malta": "MLT", "Netherlands": "NLD",
    "Poland": "POL", "Portugal": "PRT", "Romania": "ROU", "Slovenia": "SVN",
    "Spain": "ESP", "Sweden": "SWE",
}
# Slovakia already has its own time series — don't overwrite
eu_rows = cbt[cbt["country_name"] == "EUROPEAN UNION"].copy()
new_rows = []
for member_name, member_iso3 in eu_members.items():
    member_df = eu_rows.copy()
    member_df["country_name"] = member_name.upper()
    member_df["iso3"] = member_iso3
    new_rows.append(member_df)
cbt = pd.concat([cbt, *new_rows], ignore_index=True)
print(f"  After EU expansion: {cbt.shape[0]} rows, {cbt['country_name'].nunique()} countries")

# Subsample to key dates where tariff rates changed
key_dates = sorted(cbt["date"].unique())
# Select ~12-15 dates spread across the timeline
if len(key_dates) > 15:
    indices = np.linspace(0, len(key_dates) - 1, 15, dtype=int)
    selected_dates = [key_dates[i] for i in indices]
else:
    selected_dates = key_dates

cbt_sub = cbt[cbt["date"].isin(selected_dates)].copy()
cbt_sub = cbt_sub.dropna(subset=["iso3"])
cbt_sub["date_str"] = cbt_sub["date"].dt.strftime("%Y-%m-%d")

# Also load existing viz6 for the static country data
viz6_old_path = os.path.join(JOINED, "viz6_world_map.csv")
viz6_old = pd.read_csv(viz6_old_path) if os.path.exists(viz6_old_path) else pd.DataFrame()

# Save the animated version as viz6_animated
save_joined(cbt_sub[["date_str", "country_name", "iso3", "effective_tariff", "total_imports", "tariff_2024"]],
            "viz6_animated.csv")

# Also create a static latest-date version for the main map
latest_date = cbt["date"].max()
viz6_latest = cbt[cbt["date"] == latest_date].copy()
viz6_latest = viz6_latest.dropna(subset=["iso3"])

# Merge with old viz6 to keep trade flow data
if "iso3" in viz6_old.columns:
    merge_cols = [c for c in viz6_old.columns if c not in viz6_latest.columns or c == "iso3"]
    viz6_new = viz6_latest.merge(viz6_old[merge_cols], on="iso3", how="left")
else:
    viz6_new = viz6_latest

save_joined(viz6_new, "viz6_world_map.csv")
print(f"  Animated: {cbt_sub.shape[0]} rows, {len(selected_dates)} dates")
print(f"  Static (latest): {viz6_new.shape[0]} countries")

# ============================================================
# TASK 4: Fed Funds -> merge into viz8
# ============================================================
print("\n" + "=" * 60)
print("TASK 4: Fed Funds Rate -> viz8 recession signal")
print("=" * 60)

ff_path = os.path.join(RAW_FRED, "fed_funds.csv")
ff = pd.read_csv(ff_path)
ff.columns = ["date", "fed_funds"]
ff["date"] = pd.to_datetime(ff["date"])
ff["fed_funds"] = pd.to_numeric(ff["fed_funds"], errors="coerce")
ff = ff[ff["date"] >= "2024-01-01"]
save_cleaned(ff, "fred_fed_funds.csv")

# Merge into viz8 (daily data needs monthly fed funds)
viz8_path = os.path.join(JOINED, "viz8_recession_signal.csv")
viz8 = pd.read_csv(viz8_path, parse_dates=["date"])

# Create a monthly-to-daily mapping for fed funds
viz8["month_start"] = viz8["date"].dt.to_period("M").dt.to_timestamp()
ff_monthly = ff.rename(columns={"date": "month_start"})
viz8 = viz8.merge(ff_monthly, on="month_start", how="left")
viz8.drop(columns=["month_start"], inplace=True)

save_joined(viz8, "viz8_recession_signal.csv")
print(f"  Fed Funds range: {ff['fed_funds'].min():.2f} - {ff['fed_funds'].max():.2f}")
print(f"  viz8 now has {viz8.columns.tolist()}")

# ============================================================
# TASK 5: Customs Duties -> cleaned
# ============================================================
print("\n" + "=" * 60)
print("TASK 5: Customs Duties Revenue")
print("=" * 60)

cd_path = os.path.join(RAW_FRED, "customs_duties.csv")
cd = pd.read_csv(cd_path)
cd.columns = ["date", "customs_duties_bn"]
cd["date"] = pd.to_datetime(cd["date"])
cd["customs_duties_bn"] = pd.to_numeric(cd["customs_duties_bn"], errors="coerce")
save_cleaned(cd, "fred_customs_duties.csv")

print(f"  Q1 2024: ${cd.iloc[0]['customs_duties_bn']:.1f}B")
print(f"  Q4 2025: ${cd.iloc[-1]['customs_duties_bn']:.1f}B")
print(f"  Increase: {cd.iloc[-1]['customs_duties_bn'] / cd.iloc[0]['customs_duties_bn']:.1f}x")

# ============================================================
# TASK 6: Update key_events.csv with new events
# ============================================================
print("\n" + "=" * 60)
print("TASK 6: Update key events")
print("=" * 60)

events_path = os.path.join(REF, "key_events.csv")
events = pd.read_csv(events_path, parse_dates=["date"])

new_events = pd.DataFrame([
    {
        "date": pd.Timestamp("2025-04-25"),
        "event_short": "Auto tariffs 25% effective",
        "event_detail": "25% tariffs on imported automobiles take effect under Section 232",
        "impact_type": "tariff_up",
        "eff_tariff_rate_approx": 22.0,
        "story_act": "I",
    },
    {
        "date": pd.Timestamp("2025-07-30"),
        "event_short": "Copper tariffs effective",
        "event_detail": "25% tariffs on copper imports take effect under Section 232",
        "impact_type": "tariff_up",
        "eff_tariff_rate_approx": 20.0,
        "story_act": "III",
    },
    {
        "date": pd.Timestamp("2026-03-05"),
        "event_short": "24 states sue to block S122",
        "event_detail": "Coalition of 24 state attorneys general files lawsuit challenging Section 122 tariff authority",
        "impact_type": "legal",
        "eff_tariff_rate_approx": 13.0,
        "story_act": "IV",
    },
])

# Only add events that don't already exist
existing_dates = set(events["date"].dt.date)
to_add = new_events[~new_events["date"].dt.date.isin(existing_dates)]

if len(to_add) > 0:
    events = pd.concat([events, to_add], ignore_index=True)
    events = events.sort_values("date").reset_index(drop=True)
    events.to_csv(events_path, index=False)
    print(f"  Added {len(to_add)} new events. Total: {len(events)}")
else:
    print(f"  No new events needed. Total: {len(events)}")

# ============================================================
# VALIDATION
# ============================================================
print("\n" + "=" * 60)
print("VALIDATION")
print("=" * 60)

checks = {
    "viz2_price_pass_through.csv": ["date", "cpi", "consumer_sentiment"],
    "viz3_who_pays.csv": ["decile", "scenario", "pct_income_lost", "usd_cost"],
    "viz4_deficit_paradox.csv": ["date"],
    "viz5_manufacturing_tradeoff.csv": ["date"],
    "viz6_world_map.csv": ["iso3"],
    "viz6_animated.csv": ["date_str", "iso3", "effective_tariff"],
    "viz7_whatif.csv": ["scenario", "eff_tariff_rate"],
    "viz8_recession_signal.csv": ["date", "yield_spread", "fed_funds"],
}

all_pass = True
for fname, required in checks.items():
    fpath = os.path.join(JOINED, fname)
    if os.path.exists(fpath):
        df = pd.read_csv(fpath)
        missing = [c for c in required if c not in df.columns]
        if missing:
            print(f"  FAIL {fname}: missing {missing}")
            all_pass = False
        else:
            print(f"  PASS {fname}: {df.shape}")
    else:
        print(f"  FAIL {fname}: not found")
        all_pass = False

# Check viz1 still intact
viz1_path = os.path.join(JOINED, "viz1_tariff_market_fear.csv")
if os.path.exists(viz1_path):
    v1 = pd.read_csv(viz1_path)
    print(f"  PASS viz1_tariff_market_fear.csv: {v1.shape}")
else:
    print("  FAIL viz1_tariff_market_fear.csv: not found")
    all_pass = False

if all_pass:
    print("\n=== ALL VALIDATIONS PASSED ===")
else:
    print("\n=== SOME VALIDATIONS FAILED ===")
