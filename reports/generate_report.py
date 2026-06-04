from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import io

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "reports"

# Load data
metrics = pd.read_csv(PROCESSED_DIR / "performance_metrics.csv")
fund_master = pd.read_csv(PROCESSED_DIR / "01_fund_master.csv")
sip = pd.read_csv(PROCESSED_DIR / "04_monthly_sip_inflows.csv")
top5 = metrics.sort_values("cagr_pct", ascending=False).head(5)

styles = getSampleStyleSheet()
story = []

# ── Helper — save chart as image ────────────────────────
def make_chart(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return Image(buf, width=450, height=250)

# ── Title ────────────────────────────────────────────────
story.append(Paragraph("Bluestock Mutual Fund Analytics", styles["Title"]))
story.append(Paragraph("Capstone Project — Data Analyst Internship", styles["Normal"]))
story.append(Spacer(1, 12))

# ── Section 1 — Overview ─────────────────────────────────
story.append(Paragraph("1. Project Overview", styles["Heading1"]))
story.append(Paragraph(
    "This project builds an end-to-end Mutual Fund Analytics Platform analyzing "
    "40 Indian mutual fund schemes across 10 fund houses. The dataset includes "
    "46,000 NAV records, 32,778 investor transactions, AUM data, SIP inflows, "
    "and portfolio holdings from 2022 to 2026.",
    styles["Normal"]
))
story.append(Spacer(1, 12))

# ── Section 2 — Methodology ──────────────────────────────
story.append(Paragraph("2. Methodology", styles["Heading1"]))
story.append(Paragraph("Data Source:", styles["Heading2"]))
story.append(Paragraph("• 10 CSV datasets provided by Bluestock Fintech", styles["Normal"]))
story.append(Paragraph("• Live NAV data fetched from mfapi.in API", styles["Normal"]))
story.append(Spacer(1, 6))
story.append(Paragraph("Data Cleaning Steps:", styles["Heading2"]))
story.append(Paragraph("• Fixed 12 missing values in SIP yoy_growth_pct column", styles["Normal"]))
story.append(Paragraph("• Converted all date columns to datetime format", styles["Normal"]))
story.append(Paragraph("• Verified zero duplicate rows across all datasets", styles["Normal"]))
story.append(Paragraph("• Validated all 40 AMFI codes match between fund_master and nav_history", styles["Normal"]))
story.append(Spacer(1, 6))
story.append(Paragraph("Tools Used:", styles["Heading2"]))
story.append(Paragraph("• Python, Pandas, NumPy — data processing", styles["Normal"]))
story.append(Paragraph("• Matplotlib, Seaborn — visualizations", styles["Normal"]))
story.append(Paragraph("• SQLite — database storage", styles["Normal"]))
story.append(Paragraph("• Streamlit — interactive dashboard", styles["Normal"]))
story.append(Paragraph("• ReportLab, python-pptx — report generation", styles["Normal"]))
story.append(Spacer(1, 12))

# ── Section 3 — Dataset Summary ──────────────────────────
story.append(Paragraph("3. Dataset Summary", styles["Heading1"]))
data = [["File", "Rows", "Description"],
        ["fund_master", "40", "Scheme details, categories, risk grades"],
        ["nav_history", "46,000", "Daily NAV prices 2022-2026"],
        ["investor_transactions", "32,778", "Buy/sell transactions"],
        ["benchmark_indices", "8,050", "NIFTY50 daily values"],
        ["portfolio_holdings", "322", "Stock holdings per fund"],]
table = Table(data, colWidths=[180, 70, 230])
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
]))
story.append(table)
story.append(Spacer(1, 12))

# ── Section 4 — Charts ───────────────────────────────────
story.append(Paragraph("4. Key Visualizations", styles["Heading1"]))

# Chart 1 — Top 5 funds by CAGR
fig, ax = plt.subplots(figsize=(8, 4))
names = top5["scheme_name"].fillna(top5["amfi_code"].astype(str)).str[:30]
ax.barh(names, top5["cagr_pct"], color="steelblue")
ax.set_title("Top 5 Funds by CAGR (%)")
ax.set_xlabel("CAGR (%)")
plt.tight_layout()
story.append(Paragraph("Chart 1: Top 5 Funds by CAGR", styles["Heading2"]))
story.append(make_chart(fig))
story.append(Spacer(1, 12))

# Chart 2 — SIP inflow trend
fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(range(len(sip)), sip["sip_inflow_crore"], color="green", marker="o", markersize=3)
ax2.set_title("Monthly SIP Inflows (₹ Crore)")
ax2.set_xlabel("Month")
ax2.set_ylabel("SIP Inflow (₹ Crore)")
plt.tight_layout()
story.append(Paragraph("Chart 2: SIP Inflow Trend", styles["Heading2"]))
story.append(make_chart(fig2))
story.append(Spacer(1, 12))

# Chart 3 — Risk vs Return
fig3, ax3 = plt.subplots(figsize=(8, 4))
ax3.scatter(metrics["cagr_pct"], metrics["sharpe_ratio"], color="purple", alpha=0.7)
ax3.set_title("Risk vs Return — CAGR vs Sharpe Ratio")
ax3.set_xlabel("CAGR (%)")
ax3.set_ylabel("Sharpe Ratio")
plt.tight_layout()
story.append(Paragraph("Chart 3: Risk vs Return", styles["Heading2"]))
story.append(make_chart(fig3))
story.append(Spacer(1, 12))

# ── Section 5 — Top Funds Table ──────────────────────────
story.append(Paragraph("5. Top 5 Funds by CAGR", styles["Heading1"]))
data2 = [["Scheme Name", "CAGR %", "Sharpe", "VaR 95%"]]
for _, row in top5.iterrows():
    name = str(row["scheme_name"])[:40] if pd.notna(row["scheme_name"]) else str(row["amfi_code"])
    data2.append([name, f"{row['cagr_pct']}%", str(row["sharpe_ratio"]), f"{row['var_95_pct']}%"])
table2 = Table(data2, colWidths=[250, 70, 70, 70])
table2.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
]))
story.append(table2)
story.append(Spacer(1, 12))

# ── Section 6 — Recommendations ─────────────────────────
story.append(Paragraph("6. Recommendations", styles["Heading1"]))
story.append(Paragraph("For Conservative Investors (Low Risk):", styles["Heading2"]))
story.append(Paragraph("• ICICI Pru Liquid Fund — CAGR 6.97%, stable returns", styles["Normal"]))
story.append(Paragraph("• Kotak Liquid Fund — Low risk, consistent growth", styles["Normal"]))
story.append(Paragraph("• SBI Magnum Gilt Fund — Government backed, very safe", styles["Normal"]))
story.append(Spacer(1, 6))
story.append(Paragraph("For Aggressive Investors (High/Very High Risk):", styles["Heading2"]))
story.append(Paragraph("• ICICI Pru Midcap Fund — CAGR 31.48%, Sharpe 1.18", styles["Normal"]))
story.append(Paragraph("• Mirae Asset Tax Saver — CAGR 30.64%, tax benefits", styles["Normal"]))
story.append(Paragraph("• SBI Small Cap Fund — CAGR 31.10%, high growth", styles["Normal"]))
story.append(Spacer(1, 12))

# ── Section 7 — Conclusion ───────────────────────────────
story.append(Paragraph("7. Conclusion", styles["Heading1"]))
story.append(Paragraph(
    "The analysis demonstrates that Indian mutual funds have delivered exceptional returns "
    "over 2022-2026. Mid and small cap funds outperformed with 28-31% CAGR. "
    "The fund recommender system helps investors choose the right fund based on "
    "their risk appetite. The Streamlit dashboard provides interactive exploration "
    "of all metrics and trends.",
    styles["Normal"]
))

# ── Build PDF ────────────────────────────────────────────
doc = SimpleDocTemplate(str(REPORTS_DIR / "Final_Report.pdf"), pagesize=letter)
doc.build(story)
print("✅ Final_Report.pdf created with charts!")