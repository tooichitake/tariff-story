"""Download and clean U.S. Census Bureau household income distribution.

Source: Census Bureau, Current Population Survey 2025 Annual Social and
Economic Supplement (ASEC), table HINC-06 "Income Distribution to
$250,000 or More for Households" — 2024 income data.

Outputs:
  data/raw/other/census_hinc06_2025.xlsx   — original XLSX, preserved
  data/cleaned/census_income_distribution.csv  — tidy long-form CSV

The cleaned CSV has one row per income bracket with columns:
  lo               (int, band low bound in USD, e.g. 25000)
  hi               (Int64, band high bound; NULL for open-ended top band)
  count_thousands  (float, households in band, thousands — Census unit)
  share_pct        (float, share of all U.S. households, %)
  label            (str, display-ready label like "$25k-$50k" or "$250k+")

Bands are reduced from Census's 42 $5k-wide bins to the 20 $25k-wide bins
the Act II pyramid uses, plus a single open "$250k+" band at the top.
"""
from __future__ import annotations
import re
import sys
import urllib.request
from pathlib import Path

import pandas as pd

HINC06_URL = "https://www2.census.gov/programs-surveys/cps/tables/hinc-06/2025/hinc06.xlsx"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "other"
CLEAN_DIR = PROJECT_ROOT / "data" / "cleaned"
RAW_XLSX = RAW_DIR / "census_hinc06_2025.xlsx"
CLEAN_CSV = CLEAN_DIR / "census_income_distribution.csv"

# Target output bins.
#   - $0–$200k: eight uniform $25k bands (Census HINC-06 offers $5k bins in
#     this range, which we aggregate cleanly).
#   - $200k–$250k: a single $50k band, because Census publishes this range
#     as one lumped bracket — splitting to $25k would be arbitrary.
#   - $250k+: one open-ended band (Census's terminal bracket covers ~10% of
#     U.S. households and doesn't break out higher incomes).
TARGET_BINS = (
    [(lo, lo + 25_000) for lo in range(0, 200_000, 25_000)]
    + [(200_000, 250_000), (250_000, None)]
)


def _download() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if RAW_XLSX.exists() and RAW_XLSX.stat().st_size > 10_000:
        print(f"[skip] {RAW_XLSX.name} already present ({RAW_XLSX.stat().st_size // 1024} KB)")
        return
    print(f"[get ] {HINC06_URL}")
    urllib.request.urlretrieve(HINC06_URL, RAW_XLSX)
    print(f"[save] {RAW_XLSX}")


def _parse_bracket(label: str) -> tuple[int, int | None]:
    """Parse a Census bracket label to (lo, hi_exclusive)."""
    if "Under" in label:
        m = re.search(r"\$([\d,]+)", label)
        return (0, int(m.group(1).replace(",", "")))
    if "and over" in label:
        m = re.search(r"\$([\d,]+)", label)
        return (int(m.group(1).replace(",", "")), None)
    m = re.search(r"\$([\d,]+) to \$([\d,]+)", label)
    lo = int(m.group(1).replace(",", ""))
    hi = int(m.group(2).replace(",", "")) + 1   # Census bands end at .999
    return (lo, hi)


def _aggregate_to_25k_bands(raw_brackets: pd.DataFrame) -> pd.DataFrame:
    """Collapse Census's native $5k bins into our $25k target bins.

    Each Census bracket is fully contained in exactly one target bin when
    target-bin widths are multiples of $5k (they are — $25k apart). So we
    just sum ``count_thousands`` for brackets whose ``lo`` falls inside
    each target bin.
    """
    rows = []
    for target_lo, target_hi in TARGET_BINS:
        if target_hi is None:
            mask = raw_brackets["lo"] >= target_lo
        else:
            mask = (raw_brackets["lo"] >= target_lo) & (raw_brackets["lo"] < target_hi)
        count = float(raw_brackets.loc[mask, "count_thousands"].sum())
        rows.append({
            "lo": target_lo,
            "hi": target_hi,
            "count_thousands": count,
        })
    out = pd.DataFrame(rows)
    total = out["count_thousands"].sum()
    out["share_pct"] = 100.0 * out["count_thousands"] / total
    out["label"] = out.apply(_make_label, axis=1)
    return out


def _make_label(row: pd.Series) -> str:
    lo = int(row["lo"])
    hi = row["hi"]
    if pd.isna(hi):
        return f"${lo // 1000}k+"
    if lo == 0:
        return f"Under ${int(hi) // 1000}k"
    return f"${lo // 1000}k-${int(hi) // 1000}k"


def _clean() -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_excel(RAW_XLSX, sheet_name=0, header=None)

    # HINC-06 layout: rows 8..49 hold one income bracket each in col 0 (label)
    # and col 1 (household count in thousands). Row 7 is the "Total" row.
    raw = df.iloc[8:50, [0, 1]].copy()
    raw.columns = ["bracket", "count_thousands"]
    raw["count_thousands"] = pd.to_numeric(raw["count_thousands"], errors="coerce")
    raw = raw.dropna(subset=["count_thousands"])
    raw[["lo", "hi"]] = raw["bracket"].apply(lambda s: pd.Series(_parse_bracket(str(s))))

    agg = _aggregate_to_25k_bands(raw)

    # Int64 preserves the NULL at the open top band; count/share stay float.
    agg["lo"] = agg["lo"].astype("int64")
    agg["hi"] = agg["hi"].astype("Int64")
    agg = agg[["lo", "hi", "count_thousands", "share_pct", "label"]]
    agg.to_csv(CLEAN_CSV, index=False)

    print(f"[save] {CLEAN_CSV}")
    print(f"[stat] {len(agg)} bands, {agg['count_thousands'].sum():,.0f}K households "
          f"({agg['share_pct'].sum():.1f}% sum check)")
    print(agg.to_string(index=False))


def main() -> int:
    _download()
    _clean()
    return 0


if __name__ == "__main__":
    sys.exit(main())
