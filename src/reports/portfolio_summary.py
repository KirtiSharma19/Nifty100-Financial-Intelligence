import os
import pandas as pd

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

INPUT_FILE = "exports/final_financial_report.csv"

OUTPUT_DIR = "reports/portfolio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "portfolio_summary.pdf")

df = pd.read_csv(INPUT_FILE)

styles = getSampleStyleSheet()

doc = SimpleDocTemplate(OUTPUT_FILE)

story = []

story.append(Paragraph("<b>Nifty100 Portfolio Summary</b>", styles["Title"]))

table_data = [[
    "Company",
    "Sector",
    "Quality",
    "ROE",
    "Net Margin",
    "PE"
]]

for _, row in df.iterrows():

    table_data.append([
        row["company_name"],
        row["broad_sector"],
        row["quality_score"],
        row["return_on_equity_pct"],
        row["net_profit_margin_pct"],
        row["pe_ratio"]
    ])

table = Table(table_data)

table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
    ("FONTSIZE", (0, 0), (-1, -1), 8),
]))

story.append(table)

doc.build(story)

print("=" * 60)
print("Portfolio Summary Generated Successfully")
print("=" * 60)
print("Companies :", len(df))
print("Saved To :", OUTPUT_FILE)