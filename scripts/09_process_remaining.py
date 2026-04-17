"""
Process remaining data:
1. Gold price from GitHub (datasets/gold-prices)
2. DFAT Australia pivot table — extract US trade data
3. Update cleaned files and re-run joins where needed
"""
import pandas as pd
import requests
import os

from pathlib import Path
BASE = str(Path(__file__).resolve().parent.parent)
RAW = os.path.join(BASE, "data", "raw")
CLEANED = os.path.join(BASE, "data", "cleaned")
JOINED = os.path.join(BASE, "data", "joined")

# ============================================================
# 1. Gold price from GitHub datasets/gold-prices
# ============================================================
print("=== Gold Price ===")
gold_url = "https://raw.githubusercontent.com/datasets/gold-prices/main/data/monthly.csv"
try:
    r = requests.get(gold_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    if r.ok:
        with open(os.path.join(RAW, "fred", "gold.csv"), "w", newline="") as f:
            f.write(r.text)
        df = pd.read_csv(os.path.join(RAW, "fred", "gold.csv"))
        print(f"  Downloaded: {df.shape}")
        print(f"  Columns: {df.columns.tolist()}")
        print(df.tail(5).to_string())

        # Clean: standardize to date + gold columns
        df.columns = [c.lower().strip() for c in df.columns]
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df = df[df["date"] >= "2024-01-01"]
            value_col = [c for c in df.columns if c != "date"][0]
            df = df.rename(columns={value_col: "gold"})
            df["gold"] = pd.to_numeric(df["gold"], errors="coerce")
            df.to_csv(os.path.join(CLEANED, "fred_gold.csv"), index=False)
            print(f"  Cleaned: {df.shape}, range {df['date'].min().date()} to {df['date'].max().date()}")
    else:
        print(f"  HTTP {r.status_code}")
except Exception as e:
    print(f"  Failed: {e}")

# Also try daily from gold-spot-downloader
print("\n  Trying daily gold from gold-spot-downloader...")
daily_url = "https://raw.githubusercontent.com/olddatasets/gold-spot-downloader/main/data/gold_daily.csv"
try:
    r = requests.get(daily_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    if r.ok and "date" in r.text.lower()[:100]:
        daily_path = os.path.join(RAW, "fred", "gold_daily.csv")
        with open(daily_path, "w", newline="") as f:
            f.write(r.text)
        df_d = pd.read_csv(daily_path)
        print(f"  Daily gold: {df_d.shape}")
        print(f"  Columns: {df_d.columns.tolist()}")
        print(df_d.tail(3).to_string())
    else:
        print(f"  HTTP {r.status_code} or unexpected format")
except Exception as e:
    print(f"  Daily gold failed: {e}")

# ============================================================
# 2. DFAT Australia — extract US bilateral trade
# ============================================================
print("\n=== DFAT Australia — US Trade ===")
dfat_path = os.path.join(RAW, "australia", "country-commodity-pivot-table-monthly-series.xlsx")

# Read Pivot sheet: header at row 15 (0-indexed), data starts row 16
df_pivot = pd.read_excel(dfat_path, sheet_name="Pivot", header=None)
print(f"  Full pivot shape: {df_pivot.shape}")

# Row 15 has "Row Labels" + date columns
header_row = 15
headers = df_pivot.iloc[header_row].tolist()
headers[0] = "commodity"

# Data starts from row 16
data = df_pivot.iloc[header_row + 1:].copy()
data.columns = headers

# Clean date columns — convert datetime to string
date_cols = [c for c in data.columns if c != "commodity" and pd.notna(c)]
print(f"  Date columns: {len(date_cols)}, from {date_cols[0]} to {date_cols[-1]}")

# Look for US-related rows
# The pivot table structure: check what the row labels look like
print(f"\n  Sample row labels (first 30):")
labels = data["commodity"].dropna().head(30).tolist()
for label in labels:
    print(f"    {label}")

# Check if there are country groupings — look for "United States" or "US"
us_rows = data[data["commodity"].astype(str).str.contains("United States|USA|US ", case=False, na=False)]
print(f"\n  Rows containing 'United States/USA': {len(us_rows)}")
if len(us_rows) > 0:
    print(us_rows["commodity"].head(10).tolist())

# Check for "Total" or "Grand Total" rows
total_rows = data[data["commodity"].astype(str).str.contains("Total|Grand", case=False, na=False)]
print(f"\n  Total rows: {len(total_rows)}")
if len(total_rows) > 0:
    for _, row in total_rows.head(5).iterrows():
        print(f"    {row['commodity']}")

# This is a pivot table with SITC codes as rows (commodities)
# The countries are probably controlled by the pivot filter, not in rows
# Let's look at the full structure more carefully
print(f"\n  Unique row prefixes (first 50):")
for label in data["commodity"].dropna().unique()[:50]:
    s = str(label)[:60]
    print(f"    {s}")
