"""
Download Yale Budget Lab data from GitHub and Kaggle datasets.
"""
import os
import subprocess
import sys

from pathlib import Path
BASE = str(Path(__file__).resolve().parent.parent)
YALE_DIR = os.path.join(BASE, "data", "raw", "yale")
KAGGLE_DIR = os.path.join(BASE, "data", "raw", "kaggle")

# ============================================================
# Yale Budget Lab — try git clone from Tariff-Aftershock repo
# ============================================================
print("=== Downloading Yale Budget Lab data ===")
REPO_URL = "https://github.com/ericrono/Tariff-Aftershock.git"
TEMP_DIR = os.path.join(BASE, "data", "raw", "_temp_yale")

try:
    print(f"Cloning {REPO_URL}...")
    result = subprocess.run(
        ["git", "clone", "--depth", "1", REPO_URL, TEMP_DIR],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode == 0:
        print("Clone successful. Looking for XLSX files...")
        for root, dirs, files in os.walk(TEMP_DIR):
            for f in files:
                if f.endswith((".xlsx", ".csv", ".xls")):
                    src = os.path.join(root, f)
                    dst = os.path.join(YALE_DIR, f)
                    import shutil
                    shutil.copy2(src, dst)
                    print(f"  Copied: {f}")
    else:
        print(f"Git clone failed: {result.stderr}")
        print("Fallback: please manually download from budgetlab.yale.edu")
except Exception as e:
    print(f"Git clone error: {e}")
    print("Fallback: please manually download from budgetlab.yale.edu")

# ============================================================
# Kaggle datasets
# ============================================================
print("\n=== Downloading Kaggle datasets ===")
try:
    import kagglehub

    print("Downloading trump-era-tariffs-by-country...")
    path1 = kagglehub.dataset_download("soulaimanebenayad/trump-era-tariffs-by-country-2025-csv-file")
    print(f"  Downloaded to: {path1}")

    print("Downloading us-tariffs-2025...")
    path2 = kagglehub.dataset_download("danielcalvoglez/us-tariffs-2025")
    print(f"  Downloaded to: {path2}")

    # Copy files to our project
    import shutil
    for src_dir in [path1, path2]:
        if os.path.isdir(src_dir):
            for f in os.listdir(src_dir):
                src = os.path.join(src_dir, f)
                dst = os.path.join(KAGGLE_DIR, f)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                    print(f"  Copied: {f}")
        elif os.path.isfile(src_dir):
            shutil.copy2(src_dir, os.path.join(KAGGLE_DIR, os.path.basename(src_dir)))
            print(f"  Copied: {os.path.basename(src_dir)}")

except Exception as e:
    print(f"Kaggle download error: {e}")
    print("Please ensure kaggle credentials are configured (~/.kaggle/kaggle.json)")

# List what we have
print("\n=== Files in data/raw/yale/ ===")
for f in os.listdir(YALE_DIR):
    size = os.path.getsize(os.path.join(YALE_DIR, f))
    print(f"  {f} ({size:,} bytes)")

print("\n=== Files in data/raw/kaggle/ ===")
for f in os.listdir(KAGGLE_DIR):
    size = os.path.getsize(os.path.join(KAGGLE_DIR, f))
    print(f"  {f} ({size:,} bytes)")
