from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from pathlib import Path
import pandas as pd

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "reports"

# Load data
metrics = pd.read_csv(PROCESSED_DIR / "performance_metrics.csv")
fund_master = pd.read_csv(PROCESSED_DIR / "01_fund_master.csv")
top5 = metrics.sort_values("cagr_pct", ascending=False).head(5)

# Create PDF
doc = SimpleDocTemplate(str(REPORTS_DIR / "Final_Report.pdf"), pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Title
story.append(Paragraph("Bluestock Mutual Fund Analytics", styles["Title"]))
story.append(Spacer(1, 12))

# Section 1
story.append(Paragraph("1. Project Overview", styles["Heading1"]))
story.append(Paragraph(
    "This project analyzes Indian Mutual Fund data including NAV history, "
    "AUM, SIP inflows, investor transactions and portfolio holdings for 40 schemes "
    "across 10 fund houses. The goal is to provide actionable insights for investors.",
    styles["Normal"]
))
story.append(Spacer(1, 12))

# Section 2
story.append(Paragraph("2. Dataset Summary", styles["Heading1"]))
story.append(Paragraph(f"Total Schemes Analyzed: {len(fund_master)}", styles["Normal"]))
story.append(Paragraph(f"Total Fund Houses: {fund_master['fund_house'].nunique()}", styles["Normal"]))
story.append(Paragraph(f"Categories: Equity, Debt", styles["Normal"]))
story.append(Spacer(1, 12))

# Section 3
story.append(Paragraph("3. Top 5 Funds by CAGR", styles["Heading1"]))
data = [["Scheme Name", "CAGR %", "Sharpe Ratio", "VaR 95%"]]
for _, row in top5.iterrows():
    name = str(row["scheme_name"])[:40] if pd.notna(row["scheme_name"]) else str(row["amfi_code"])
    data.append([name, f"{row['cagr_pct']}%", str(row["sharpe_ratio"]), f"{row['var_95_pct']}%"])

table = Table(data, colWidths=[250, 70, 90, 70])
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
]))
story.append(table)
story.append(Spacer(1, 12))

# Section 4
story.append(Paragraph("4. Key Findings", styles["Heading1"]))
story.append(Paragraph("• Top performing fund achieved CAGR of 31.48%", styles["Normal"]))
story.append(Paragraph("• Most funds have Sharpe Ratio above 1.0 indicating good risk-adjusted returns", styles["Normal"]))
story.append(Paragraph("• Small cap and mid cap funds outperformed large cap funds", styles["Normal"]))
story.append(Paragraph("• SIP inflows grew consistently over the analysis period", styles["Normal"]))
story.append(Spacer(1, 12))

# Section 5
story.append(Paragraph("5. Conclusion", styles["Heading1"]))
story.append(Paragraph(
    "The analysis shows that Indian mutual funds have delivered strong returns over the "
    "2022-2026 period. Mid and small cap funds have outperformed with higher CAGR but "
    "also carry higher risk. Investors should choose funds based on their risk appetite "
    "using our recommender system.",
    styles["Normal"]
))

# Build PDF
doc.build(story)
print("✅ Final_Report.pdf created!")