from src.services.ratio_engine import DatasetBuilder

engine = DatasetBuilder()

df = engine.build_dataset()

columns = [
    "company_name",
    "broad_sector",
    "year",
    "quality_score",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "capex_cr",
    "cash_from_operations_cr"
]

report = df[columns]

report.to_csv(
    "exports/final_financial_report.csv",
    index=False
)

print()
print("Final Financial Report Generated")
print(report.head())