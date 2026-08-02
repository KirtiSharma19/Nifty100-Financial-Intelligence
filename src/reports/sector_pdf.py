import os
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

INPUT_FILE = "exports/sector_report.csv"
OUTPUT_DIR = "reports/sector"

os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

styles = getSampleStyleSheet()

print("=" * 60)
print("Generating Sector PDFs...")
print("=" * 60)

for _, row in df.iterrows():

    sector = str(row["broad_sector"]).replace("/", "-").replace("\\", "-")

    pdf_file = os.path.join(
        OUTPUT_DIR,
        f"{sector}_report.pdf"
    )

    doc = SimpleDocTemplate(pdf_file)

    story = []

    story.append(
        Paragraph(
            f"<b>{sector} Sector Report</b>",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 20))

    data = [
        ["Metric", "Value"],
        ["Average Quality Score", row["quality_score"]],
        ["Average ROE", row["return_on_equity_pct"]],
        ["Average Net Profit Margin", row["net_profit_margin_pct"]],
        ["Average Debt To Equity", row["debt_to_equity"]],
    ]

    table = Table(data)

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )

    story.append(table)

    doc.build(story)

    print("Generated :", sector)

print("=" * 60)
print("Sector PDFs Generated Successfully")
print("=" * 60)
print("Total Sectors :", len(df))
print("Saved To :", OUTPUT_DIR)