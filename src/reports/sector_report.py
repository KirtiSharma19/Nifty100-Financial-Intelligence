from src.services.ratio_engine import DatasetBuilder

engine = DatasetBuilder()

df = engine.build_dataset()

sector_report = (
    df.groupby("broad_sector")
    .agg(
        {
            "quality_score": "mean",
            "net_profit_margin_pct": "mean",
            "return_on_equity_pct": "mean",
            "debt_to_equity": "mean",
        }
    )
    .round(2)
    .sort_values("quality_score", ascending=False)
)

sector_report.to_csv("exports/sector_report.csv")

print()
print("Sector Report Generated Successfully")
print()
print(sector_report)
