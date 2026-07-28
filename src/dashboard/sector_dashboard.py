from src.services.ratio_engine import DatasetBuilder

engine = DatasetBuilder()

df = engine.build_dataset()

sector_summary = (
    df.groupby("broad_sector")
    .agg(
        companies=("company_name", "nunique"),
        avg_quality=("quality_score", "mean"),
        avg_roe=("return_on_equity_pct", "mean"),
        avg_margin=("net_profit_margin_pct", "mean"),
        avg_debt=("debt_to_equity", "mean"),
    )
    .round(2)
    .sort_values("avg_quality", ascending=False)
)

print()
print("=" * 80)
print("SECTOR DASHBOARD")
print("=" * 80)
print(sector_summary)