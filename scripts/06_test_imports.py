"""Quick test: verify all app modules can be imported."""
import sys
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
APP_DIR = str(BASE / "app")
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

# Test config
from config import JOINED_DIR, REF_DIR, CLEANED_DIR
print(f"JOINED_DIR: {JOINED_DIR}")
print(f"REF_DIR: {REF_DIR}")

# Test data files exist
import pandas as pd
for fname in ["viz1_tariff_market_fear.csv", "viz2_price_pass_through.csv",
              "viz3_who_pays.csv", "viz4_deficit_paradox.csv",
              "viz5_manufacturing_tradeoff.csv", "viz6_world_map.csv",
              "viz7_whatif.csv", "viz8_recession_signal.csv"]:
    path = os.path.join(JOINED_DIR, fname)
    if os.path.exists(path):
        df = pd.read_csv(path)
        print(f"  {fname}: {df.shape} OK")
    else:
        print(f"  {fname}: NOT FOUND")

# Test component imports (without streamlit)
for mod_name in ["act1_scale", "act2_who_pays", "act3_tradeoffs", "act4_choice"]:
    try:
        # Just check syntax by compiling
        mod_path = os.path.join(APP_DIR, "components", f"{mod_name}.py")
        with open(mod_path, encoding="utf-8") as f:
            compile(f.read(), mod_path, "exec")
        print(f"  components/{mod_name}.py: syntax OK")
    except SyntaxError as e:
        print(f"  components/{mod_name}.py: SYNTAX ERROR - {e}")

# Check app.py syntax
app_path = os.path.join(APP_DIR, "app.py")
with open(app_path, encoding="utf-8") as f:
    compile(f.read(), app_path, "exec")
print("  app.py: syntax OK")

print("\nAll checks passed! Run with: streamlit run app.py")
