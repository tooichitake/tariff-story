import requests
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "raw" / "fred" / "gold.csv"

candidates = ["GOLDAMGBD228NLBM", "GLDPRZS"]
for sid in candidates:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&cosd=2024-01-01&coed=2026-04-08"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    if r.ok:
        lines = r.text.strip().split("\n")
        print(f"{sid}: {r.status_code} - {len(lines)-1} rows")
        with open(OUT, "w", newline="") as f:
            f.write(r.text)
        print("Saved!")
        break
    else:
        print(f"{sid}: {r.status_code} FAIL")
