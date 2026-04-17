"""
Phase 2: Clean all downloaded data (FRED, Yale, Kaggle).
- FRED: replace "." with NaN, standardize dates, filter 2024+
- Yale: parse XLSX sheets and CSV outputs
- Kaggle: standardize country names to ISO3
"""
import pandas as pd
import os

from pathlib import Path
BASE = str(Path(__file__).resolve().parent.parent)
RAW_FRED = os.path.join(BASE, "data", "raw", "fred")
RAW_YALE = os.path.join(BASE, "data", "raw", "yale")
RAW_KAGGLE = os.path.join(BASE, "data", "raw", "kaggle")
CLEANED = os.path.join(BASE, "data", "cleaned")
REF = os.path.join(BASE, "data", "reference")

# ============================================================
# 2A. Clean FRED data
# ============================================================
print("=== Cleaning FRED data ===")

FRED_FILES = {
    "sp500": "sp500",
    "cpi": "cpi",
    "usd_index": "usd_index",
    "gold": "gold",
    "vix": "vix",
    "treasury_10y": "treasury_10y",
    "yield_spread": "yield_spread",
    "gdp_growth": "gdp_growth",
    "trade_balance": "trade_balance",
    "industrial_prod": "industrial_prod",
    "unemployment": "unemployment",
    "mfg_employment": "mfg_employment",
    "mfg_job_openings": "mfg_job_openings",
}

for name, outname in FRED_FILES.items():
    filepath = os.path.join(RAW_FRED, f"{name}.csv")
    if not os.path.exists(filepath):
        print(f"  SKIP {name} (file not found)")
        continue

    df = pd.read_csv(filepath)
    # Rename columns: first col = date, second col = value name
    cols = df.columns.tolist()
    df.rename(columns={cols[0]: "date", cols[1]: outname}, inplace=True)

    # Convert date
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Replace "." with NaN and convert to numeric
    df[outname] = pd.to_numeric(df[outname], errors="coerce")

    # Filter to 2024+
    df = df[df["date"] >= "2024-01-01"].copy()
    df = df.dropna(subset=["date"])

    outpath = os.path.join(CLEANED, f"fred_{outname}.csv")
    df.to_csv(outpath, index=False)

    nan_count = df[outname].isna().sum()
    print(f"  [OK] fred_{outname}.csv: {df.shape[0]} rows, "
          f"date range {df['date'].min().date()} to {df['date'].max().date()}, "
          f"{nan_count} NaN")

# ============================================================
# 2B. Clean Yale data
# ============================================================
print("\n=== Cleaning Yale data ===")

# Yale CSV outputs from the Tariff-Aftershock repo
yale_csvs = {
    "output_commodity_prices.csv": "yale_commodity_prices.csv",
    "output_country_gdp.csv": "yale_country_gdp.csv",
    "output_regional_tariffs.csv": "yale_regional_tariffs.csv",
    "output_revenue_forecast.csv": "yale_revenue_forecast.csv",
    "output_revenue_projections.csv": "yale_revenue_projections.csv",
    "output_sectoral_gdp.csv": "yale_sectoral_gdp.csv",
    "output_summary_metrics.csv": "yale_summary_metrics.csv",
}

for src, dst in yale_csvs.items():
    filepath = os.path.join(RAW_YALE, src)
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        df.to_csv(os.path.join(CLEANED, dst), index=False)
        print(f"  [OK] {dst}: {df.shape}")
    else:
        print(f"  SKIP {src} (not found)")

# Parse the Yale XLSX for distributional data (F5 sheet)
xlsx_path = os.path.join(RAW_YALE, "TBL-Data-February-Tariffs-202602_0.xlsx")
if os.path.exists(xlsx_path):
    print(f"\n  Exploring Yale XLSX sheets...")
    xl = pd.ExcelFile(xlsx_path)
    print(f"  Sheets: {xl.sheet_names}")

    for sheet in xl.sheet_names:
        df = pd.read_excel(xlsx_path, sheet_name=sheet, header=None, nrows=5)
        print(f"\n  --- {sheet} (first 5 rows) ---")
        print(df.to_string())

    # Try to extract F5 (distributional) if it exists
    for sheet in xl.sheet_names:
        if "F5" in sheet or "distribut" in sheet.lower():
            print(f"\n  Extracting distributional data from sheet: {sheet}")
            df_full = pd.read_excel(xlsx_path, sheet_name=sheet, header=None)
            df_full.to_csv(os.path.join(CLEANED, "yale_distributional_raw.csv"), index=False)
            print(f"  Saved raw extraction: {df_full.shape}")

    # Try T2 (regional tariffs)
    for sheet in xl.sheet_names:
        if "T2" in sheet or "region" in sheet.lower():
            print(f"\n  Extracting regional tariffs from sheet: {sheet}")
            df_full = pd.read_excel(xlsx_path, sheet_name=sheet, header=None)
            df_full.to_csv(os.path.join(CLEANED, "yale_regional_tariffs_raw.csv"), index=False)
            print(f"  Saved raw extraction: {df_full.shape}")

# ============================================================
# 2C. Clean Kaggle data
# ============================================================
print("\n=== Cleaning Kaggle data ===")

# Load country mapping for ISO3 standardization
country_map = pd.read_csv(os.path.join(REF, "country_mapping.csv"))
name_to_iso3 = dict(zip(country_map["name_variant"], country_map["iso3"]))

for fname in os.listdir(RAW_KAGGLE):
    filepath = os.path.join(RAW_KAGGLE, fname)
    if not fname.endswith(".csv"):
        continue

    try:
        df = pd.read_csv(filepath, on_bad_lines="skip")
    except Exception as e:
        print(f"\n  ERROR reading {fname}: {e}")
        continue
    print(f"\n  {fname}: {df.shape}")
    print(f"  Columns: {df.columns.tolist()}")
    print(df.head(3).to_string())

    # Try to add ISO3 codes
    country_col = None
    for col in df.columns:
        if "country" in col.lower() or "nation" in col.lower():
            country_col = col
            break

    if country_col:
        df["iso3"] = df[country_col].map(name_to_iso3)
        mapped = df["iso3"].notna().sum()
        unmapped = df[df["iso3"].isna()][country_col].unique()
        print(f"  ISO3 mapped: {mapped}/{len(df)}")
        if len(unmapped) > 0:
            print(f"  Unmapped countries: {unmapped[:10]}")

    # Standardize column names
    df.columns = [c.strip().lower().replace(" ", "_").replace("(%)", "pct").replace("($)", "usd") for c in df.columns]

    outname = fname.replace(" ", "_").lower()
    df.to_csv(os.path.join(CLEANED, f"kaggle_{outname}"), index=False)
    print(f"  -> Saved: kaggle_{outname}")

print("\n=== All data cleaning complete ===")

# Summary
print("\n=== Cleaned files ===")
for f in sorted(os.listdir(CLEANED)):
    size = os.path.getsize(os.path.join(CLEANED, f))
    print(f"  {f} ({size:,} bytes)")
