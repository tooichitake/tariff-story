"""Explore downloaded GTA alternative data."""
import pandas as pd
import os
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from pathlib import Path
BASE = str(Path(__file__).resolve().parent.parent / "data" / "raw" / "other")

# 1. Kratosfury Tariffs-USA XLSX
print("=== gta_tariffs_usa.xlsx ===")
xl = pd.ExcelFile(os.path.join(BASE, "gta_tariffs_usa.xlsx"))
print(f"Sheets: {xl.sheet_names}")
for sheet in xl.sheet_names[:3]:
    df = pd.read_excel(xl, sheet_name=sheet, header=None, nrows=10)
    print(f"\n  {sheet}: {df.shape}")
    print(df.to_string())

# 2. Whitehouse tariffs
print("\n\n=== whitehouse_trump_tariffs_20250402.csv ===")
df = pd.read_csv(os.path.join(BASE, "whitehouse_trump_tariffs_20250402.csv"))
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(df.head(10).to_string())

# 3. Daily tariff
print("\n\n=== tradewar_daily_tariff.csv ===")
df = pd.read_csv(os.path.join(BASE, "tradewar_daily_tariff.csv"))
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(df.head(5).to_string())
print("...")
print(df.tail(5).to_string())

# 4. Federal tax duty
print("\n\n=== tradewar_federal-tax-duty.csv ===")
df = pd.read_csv(os.path.join(BASE, "tradewar_federal-tax-duty.csv"))
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(df.head(5).to_string())
