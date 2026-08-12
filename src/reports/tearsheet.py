import os

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# -------------------------------------------------

INPUT_FILE = "exports/final_financial_report.csv"

OUTPUT_FOLDER = "reports/tearsheets"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

styles = getSampleStyleSheet()

print("=" * 60)
print("Generating Company Tearsheets...")
print("=" * 60)

# -------------------------------------------------
# Generate one PDF for each company
# -------------------------------------------------

for _, row in df.iterrows():

    import re

    company = str(row["company_name"]).strip()

    company = re.sub(r'[\\/:*?"<>|\r\n]+', "_", company)

    company = company.replace("&", "and")

    filename = f"{company}_tearsheet.pdf"

    pdf_file = os.path.join(OUTPUT_FOLDER, filename)

    doc = SimpleDocTemplate(pdf_file)

    story = []

    # -------------------------------------------------

    title = Paragraph(f"<b>{company}</b>", styles["Title"])

    story.append(title)
    story.append(Spacer(1, 0.25 * inch))

    story.append(Paragraph(f"<b>Sector:</b> {row['broad_sector']}", styles["Normal"]))

    story.append(Spacer(1, 0.20 * inch))

    # -------------------------------------------------

    table_data = [
        ["Metric", "Value"],
        ["Quality Score", row["quality_score"]],
        ["ROE %", row["return_on_equity_pct"]],
        ["Net Profit Margin %", row["net_profit_margin_pct"]],
        ["Debt / Equity", row["debt_to_equity"]],
        ["Free Cash Flow (Cr)", row["free_cash_flow_cr"]],
        ["Market Cap (Cr)", row["market_cap_crore"]],
        ["Enterprise Value (Cr)", row["enterprise_value_crore"]],
        ["PE Ratio", row["pe_ratio"]],
        ["PB Ratio", row["pb_ratio"]],
        ["EV / EBITDA", row["ev_ebitda"]],
        ["Dividend Yield %", row["dividend_yield_pct"]],
    ]

    table = Table(table_data)

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )

    story.append(table)
    print(repr(company))
    doc.build(story)

    print(f"Generated : {company}")

    print("=" * 60)
    print("All Company Tearsheets Generated Successfully")
    print("=" * 60)

    print(f"Total Companies : {len(df)}")
    print(f"Saved To : {OUTPUT_FOLDER}")
