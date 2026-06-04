import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Load data
nav_history = pd.read_csv(PROCESSED_DIR / "02_nav_history.csv", parse_dates=["date"])
fund_master = pd.read_csv(PROCESSED_DIR / "01_fund_master.csv")
performance = pd.read_csv(PROCESSED_DIR / "07_scheme_performance.csv")
metrics = pd.read_csv(PROCESSED_DIR / "performance_metrics.csv")

# Title
st.title("🏦 Bluestock Mutual Fund Dashboard")
st.markdown("Interactive analytics for Indian Mutual Funds")

# ── Page 1 — Fund Overview ───────────────────────────────
st.header("📋 Fund Overview")

# Slicer 1 — Fund House filter
fund_houses = ["All"] + list(fund_master["fund_house"].unique())
selected_house = st.selectbox("Select Fund House", fund_houses)

# Slicer 2 — Category filter
categories = ["All"] + list(fund_master["category"].unique())
selected_category = st.selectbox("Select Category", categories)

# Filter data
filtered = fund_master.copy()
if selected_house != "All":
    filtered = filtered[filtered["fund_house"] == selected_house]
if selected_category != "All":
    filtered = filtered[filtered["category"] == selected_category]

st.dataframe(filtered[["scheme_name", "fund_house", "category", "risk_category", "expense_ratio_pct"]])

# ── Page 2 — NAV Growth ──────────────────────────────────
st.header("📈 NAV Growth Over Time")

# Slicer — scheme selector
scheme_names = fund_master["scheme_name"].tolist()
selected_scheme = st.selectbox("Select Scheme", scheme_names)

selected_code = fund_master[fund_master["scheme_name"] == selected_scheme]["amfi_code"].values[0]
scheme_nav = nav_history[nav_history["amfi_code"] == selected_code]

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(scheme_nav["date"], scheme_nav["nav"], color="blue")
ax.set_title(f"NAV Growth — {selected_scheme}")
ax.set_xlabel("Date")
ax.set_ylabel("NAV (₹)")
st.pyplot(fig)

# ── Page 3 — Performance Metrics ────────────────────────
st.header("🏆 Performance Metrics")

# Slicer — sort by
sort_by = st.selectbox("Sort By", ["cagr_pct", "sharpe_ratio", "var_95_pct"])
sorted_metrics = metrics.sort_values(sort_by, ascending=False)
st.dataframe(sorted_metrics)

# ── Page 4 — Top Performers ──────────────────────────────
st.header("🥇 Top 10 Performers by CAGR")

top10 = metrics.sort_values("cagr_pct", ascending=False).head(10)
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.barh(top10["scheme_name"].fillna(top10["amfi_code"].astype(str)), top10["cagr_pct"], color="green")
ax2.set_xlabel("CAGR (%)")
ax2.set_title("Top 10 Funds by CAGR")
plt.tight_layout()
st.pyplot(fig2)

st.success("Dashboard loaded successfully! ✅")