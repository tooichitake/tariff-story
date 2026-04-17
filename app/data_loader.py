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
