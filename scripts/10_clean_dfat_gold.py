"""Clean DFAT and gold data, integrate into joined datasets."""
import pandas as pd
import os

from pathlib import Path
BASE = str(Path(__file__).resolve().parent.parent)
CLEANED = os.path.join(BASE, "data", "cleaned")
JOINED = os.path.join(BASE, "data", "joined")
RAW = os.path.join(BASE, "data", "raw")

# ============================================================
# 1. DFAT — extract top export commodities (total Australia)
# ============================================================
print("=== DFAT Commodity Trade ===")
dfat_path = os.path.join(RAW, "australia", "country-commodity-pivot-table-monthly-series.xlsx")

df_pivot = pd.read_excel(dfat_path, sheet_name="Pivot", header=None)
header_row = 15
headers = df_pivot.iloc[header_row].tolist()
headers[0] = "commodity"

data = df_pivot.iloc[header_row + 1:].copy()
data.columns = headers

# Convert date columns to proper format
date_cols = [c for c in data.columns if c != "commodity" and pd.notna(c)]

# Melt to long format: commodity, date, value
data_long = data.melt(id_vars=["commodity"], value_vars=date_cols,
                       var_name="date", value_name="trade_value_aud_thousands")
data_long["date"] = pd.to_datetime(data_long["date"])
data_long["trade_value_aud_thousands"] = pd.to_numeric(
    data_long["trade_value_aud_thousands"], errors="coerce"
)

# Filter to 2024+ and drop NaN
data_long = data_long[data_long["date"] >= "2024-01-01"].dropna(subset=["trade_value_aud_thousands"])
data_long = data_long[data_long["commodity"] != "Grand Total"]

# Save full cleaned DFAT data
data_long.to_csv(os.path.join(CLEANED, "dfat_commodity_monthly.csv"), index=False)
print(f"  Cleaned DFAT: {data_long.shape}")

# Top 10 commodities by total trade value (2024+)
top_commodities = (data_long.groupby("commodity")["trade_value_aud_thousands"]
                   .sum()
                   .sort_values(ascending=False)
                   .head(15))
print(f"\n  Top 15 Australian export commodities (2024+, AUD thousands):")
for commodity, value in top_commodities.items():
    print(f"    {commodity}: {value:,.0f}")

# Grand total by month
grand_total = data[data["commodity"] == "Grand Total"]
if len(grand_total) > 0:
    gt_row = grand_total.iloc[0]
    monthly_totals = []
    for col in date_cols:
        val = pd.to_numeric(gt_row[col], errors="coerce")
        if pd.notna(val):
            monthly_totals.append({"date": pd.to_datetime(col), "total_trade_aud_thousands": val})
    gt_df = pd.DataFrame(monthly_totals)
    gt_df = gt_df[gt_df["date"] >= "2024-01-01"]
    gt_df.to_csv(os.path.join(CLEANED, "dfat_monthly_total.csv"), index=False)
    print(f"\n  Monthly totals: {gt_df.shape}")
    print(gt_df.tail(5).to_string(index=False))

# ============================================================
# 2. Verify gold price is in cleaned data
# ============================================================
print("\n=== Gold Price Check ===")
gold_path = os.path.join(CLEANED, "fred_gold.csv")
if os.path.exists(gold_path):
    gold = pd.read_csv(gold_path, parse_dates=["date"])
    print(f"  Gold: {gold.shape}, range {gold['date'].min().date()} to {gold['date'].max().date()}")
    print(gold.tail(5).to_string(index=False))
else:
    print("  Gold not found in cleaned!")

# ============================================================
# 3. Summary of all data files
# ============================================================
print("\n=== COMPLETE DATA INVENTORY ===")
for subdir in ["raw/fred", "raw/kaggle", "raw/yale", "raw/australia", "cleaned", "joined", "reference"]:
    dirpath = os.path.join(BASE, "data", subdir)
    if os.path.exists(dirpath):
        files = [f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))]
        total = sum(os.path.getsize(os.path.join(dirpath, f)) for f in files)
        print(f"\n  {subdir}/: {len(files)} files, {total:,.0f} bytes")
        for f in sorted(files):
            size = os.path.getsize(os.path.join(dirpath, f))
            print(f"    {f} ({size:,} bytes)")
