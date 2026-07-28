from src.services.ratio_engine import DatasetBuilder

engine = DatasetBuilder()

df = engine.build_dataset()

company = "Abbott India Ltd"

company_df = df[
    df["company_name"] == company
]

print(company_df[
    [
        "year",
        "quality_score",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "debt_to_equity",
        "return_on_equity_pct",
        "free_cash_flow_cr"
    ]
])