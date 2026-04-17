"""
Download 11 FRED economic series as CSV files.
Each file: 2 columns (DATE, value), date range 2024-01-01 to 2026-04-08.
"""
import requests
import os
import time

from pathlib import Path
BASE = str(Path(__file__).resolve().parent.parent)
FRED_DIR = os.path.join(BASE, "data", "raw", "fred")

FRED_SERIES = {
    "sp500": "SP500",
    "cpi": "CPIAUCSL",
    "usd_index": "DTWEXBGS",
    "gold": "GOLDPMGBD228NLBM",
    "vix": "VIXCLS",
    "treasury_10y": "DGS10",
    "yield_spread": "T10Y2Y",
    "gdp_growth": "A191RL1Q225SBEA",
    "trade_balance": "BOPGSTB",
    "industrial_prod": "INDPRO",
    "unemployment": "UNRATE",
}

START = "2024-01-01"
END = "2026-04-08"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

success = []
failed = []

for name, series_id in FRED_SERIES.items():
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={START}&coed={END}"
    filepath = os.path.join(FRED_DIR, f"{name}.csv")

    try:
        print(f"Downloading {name} ({series_id})...", end=" ")
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()

        with open(filepath, "w", newline="") as f:
            f.write(resp.text)

        lines = resp.text.strip().split("\n")
        print(f"OK - {len(lines)-1} rows")
        success.append(name)
    except Exception as e:
        print(f"FAILED - {e}")
        failed.append((name, url))

    time.sleep(0.5)  # polite delay

print(f"\n=== Results: {len(success)} OK, {len(failed)} failed ===")

if failed:
    print("\nFailed downloads - open these URLs in browser:")
    for name, url in failed:
        print(f"  {name}: {url}")
        print(f"  Save to: {os.path.join(FRED_DIR, name + '.csv')}")
