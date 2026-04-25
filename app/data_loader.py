"""Cached data loading for all visualization datasets."""
import pandas as pd
import streamlit as st
import os
from config import JOINED_DIR, REF_DIR, CLEANED_DIR


@st.cache_data
def load_viz1():
    return pd.read_csv(os.path.join(JOINED_DIR, "viz1_tariff_market_fear.csv"), parse_dates=["date"])


@st.cache_data
def load_viz2():
    return pd.read_csv(os.path.join(JOINED_DIR, "viz2_price_pass_through.csv"), parse_dates=["date"])


@st.cache_data
def load_viz3():
    return pd.read_csv(os.path.join(JOINED_DIR, "viz3_who_pays.csv"))


@st.cache_data
def load_viz4():
    return pd.read_csv(os.path.join(JOINED_DIR, "viz4_deficit_paradox.csv"), parse_dates=["date"])


@st.cache_data
def load_viz5():
    return pd.read_csv(os.path.join(JOINED_DIR, "viz5_manufacturing_tradeoff.csv"), parse_dates=["date"])


@st.cache_data
def load_viz6():
    return pd.read_csv(os.path.join(JOINED_DIR, "viz6_world_map.csv"))


@st.cache_data
def load_viz6_consumer():
    path = os.path.join(JOINED_DIR, "viz6_consumer_map.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


@st.cache_data
def load_viz6_animated():
    path = os.path.join(JOINED_DIR, "viz6_animated.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


@st.cache_data
def load_viz7():
    return pd.read_csv(os.path.join(JOINED_DIR, "viz7_whatif.csv"))


@st.cache_data
def load_viz8():
    return pd.read_csv(os.path.join(JOINED_DIR, "viz8_recession_signal.csv"), parse_dates=["date"])


@st.cache_data
def load_key_events():
    return pd.read_csv(os.path.join(REF_DIR, "key_events.csv"), parse_dates=["date"])


@st.cache_data
def load_commodity_prices():
    path = os.path.join(CLEANED_DIR, "yale_commodity_prices.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


@st.cache_data
def load_customs_duties():
    path = os.path.join(CLEANED_DIR, "fred_customs_duties.csv")
    if os.path.exists(path):
        return pd.read_csv(path, parse_dates=["date"])
    return None


@st.cache_data
def load_us_income_distribution():
    """U.S. household income distribution by $25k income band.

    Source: U.S. Census Bureau, CPS ASEC 2025 (HINC-06), for 2024 income.
    Aggregated from the native $5k bins into 10 reader-friendly bands:
    eight $25k-wide bands from $0 to $200k, one $50k band for $200-250k
    (Census publishes that range lumped), and one open "$250k+" band.

    Cols: lo, hi (Int64; NULL for open band), count_thousands, share_pct,
    label. Used by the Act II "Where Americans live" pyramid; refresh
    via ``scripts/15_download_census_income.py``.
    """
    path = os.path.join(CLEANED_DIR, "census_income_distribution.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return None
