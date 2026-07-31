import pandas as pd

from src.services.ratio_engine import DatasetBuilder


def generate_final_report():

    engine = DatasetBuilder()

    df = engine.build_dataset()

    latest_year = df["year"].max()

    latest = df[df["year"] == latest_year].copy()

    report = latest[
        [
            "company_name",
            "broad_sector",
            "quality_score",
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "market_cap_crore",
            "enterprise_value_crore",
            "pe_ratio",
            "pb_ratio",
            "ev_ebitda",
            "dividend_yield_pct",
        ]
    ].sort_values(
        "quality_score",
        ascending=False
    )

    report.to_csv(
        "exports/final_financial_report.csv",
        index=False
    )

    print()
    print("=" * 60)
    print("FINAL REPORT GENERATED")
    print("=" * 60)
    print()

    print(report.head(10))

    print()
    print("Rows :", len(report))
    print()
    print("Saved -> exports/final_financial_report.csv")


if __name__ == "__main__":
    generate_final_report()