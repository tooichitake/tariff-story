"""Explore DFAT XLSX structure — MUST use header=None, nrows=20 first."""
import pandas as pd
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
path = str(BASE / "data" / "raw" / "australia" / "country-commodity-pivot-table-monthly-series.xlsx")

xl = pd.ExcelFile(path)
print(f"Sheets: {xl.sheet_names}")

for sheet in xl.sheet_names[:5]:
    print(f"\n=== Sheet: {sheet} ===")
    df = pd.read_excel(path, sheet_name=sheet, header=None, nrows=20)
    print(f"Shape (first 20 rows): {df.shape}")
    print(df.to_string())
