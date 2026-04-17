"""
Download GTA tariff data alternatives from GitHub:
1. Kratosfury/Tariffs-USA — US tariff XLSX
2. tradewartracker/trade-war-redux-2025 — tariff analysis data
3. Budget-Lab-Yale/Tariff-ETRs — Yale ETR data
4. Whitehouse Trump Tariffs gist
"""
import requests
import os

from pathlib import Path
BASE = str(Path(__file__).resolve().parent.parent)
GTA_DIR = os.path.join(BASE, "data", "raw", "other")
HEADERS = {"User-Agent": "Mozilla/5.0"}

downloads = [
    # Kratosfury Tariffs-USA XLSX
    (
        "https://raw.githubusercontent.com/Kratosfury/Tariffs-USA/main/Tariff.xlsx",
        "gta_tariffs_usa.xlsx",
    ),
    # Trump tariffs CSV from gist
    (
        "https://gist.githubusercontent.com/mcoliver/69fe48d03c12388e29cc0cd87eb44df6/raw/Whitehouse%20Trump%20Tariffs%2020205-04-02.csv",
        "whitehouse_trump_tariffs_20250402.csv",
    ),
]

for url, fname in downloads:
    path = os.path.join(GTA_DIR, fname)
    print(f"Downloading {fname}...", end=" ")
    try:
        r = requests.get(url, headers=HEADERS, timeout=60)
        if r.ok:
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"OK - {len(r.content):,} bytes")
        else:
            print(f"HTTP {r.status_code}")
    except Exception as e:
        print(f"FAILED: {e}")

# Try trade-war-redux-2025 repo for CSV data files
print("\nChecking tradewartracker/trade-war-redux-2025...")
api_url = "https://api.github.com/repos/tradewartracker/trade-war-redux-2025/contents/data"
try:
    r = requests.get(api_url, headers=HEADERS, timeout=15)
    if r.ok:
        files = r.json()
        for f in files:
            if f["name"].endswith((".csv", ".xlsx", ".json")):
                print(f"  Found: {f['name']} ({f.get('size', '?')} bytes)")
                dl = requests.get(f["download_url"], headers=HEADERS, timeout=30)
                if dl.ok:
                    with open(os.path.join(GTA_DIR, f"tradewar_{f['name']}"), "wb") as out:
                        out.write(dl.content)
                    print(f"    Downloaded!")
    else:
        # Try root directory
        api_url2 = "https://api.github.com/repos/tradewartracker/trade-war-redux-2025/contents/"
        r2 = requests.get(api_url2, headers=HEADERS, timeout=15)
        if r2.ok:
            files = r2.json()
            csv_files = [f for f in files if f["name"].endswith((".csv", ".xlsx"))]
            for f in csv_files:
                print(f"  Found: {f['name']}")
                dl = requests.get(f["download_url"], headers=HEADERS, timeout=30)
                if dl.ok:
                    with open(os.path.join(GTA_DIR, f"tradewar_{f['name']}"), "wb") as out:
                        out.write(dl.content)
                    print(f"    Downloaded!")
        else:
            print(f"  HTTP {r2.status_code}")
except Exception as e:
    print(f"  Failed: {e}")

# Check Yale Budget Lab Tariff-ETRs for data
print("\nChecking Budget-Lab-Yale/Tariff-ETRs...")
api_url3 = "https://api.github.com/repos/Budget-Lab-Yale/Tariff-ETRs/contents/"
try:
    r = requests.get(api_url3, headers=HEADERS, timeout=15)
    if r.ok:
        files = r.json()
        for f in files:
            print(f"  {f['name']} ({'dir' if f['type'] == 'dir' else f.get('size', '?')})")
            if f["type"] == "dir" and f["name"] in ["data", "output", "results"]:
                subr = requests.get(f["url"], headers=HEADERS, timeout=15)
                if subr.ok:
                    for sf in subr.json():
                        if sf["name"].endswith((".csv", ".xlsx", ".rds")):
                            print(f"    {sf['name']} ({sf.get('size', '?')} bytes)")
                            if sf["name"].endswith(".csv") and sf.get("size", 0) < 5_000_000:
                                dl = requests.get(sf["download_url"], headers=HEADERS, timeout=30)
                                if dl.ok:
                                    with open(os.path.join(GTA_DIR, f"yale_etr_{sf['name']}"), "wb") as out:
                                        out.write(dl.content)
                                    print(f"      Downloaded!")
    else:
        print(f"  HTTP {r.status_code}")
except Exception as e:
    print(f"  Failed: {e}")

# Summary
print("\n=== Files in data/raw/other/ ===")
for f in sorted(os.listdir(GTA_DIR)):
    size = os.path.getsize(os.path.join(GTA_DIR, f))
    print(f"  {f} ({size:,} bytes)")
