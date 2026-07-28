from src.services.ratio_engine import DatasetBuilder

engine = DatasetBuilder()

df = engine.build_dataset()

sector_summary = (
    df.groupby("broad_sector")
    .agg(
        {
            "quality_score": "mean",
            "net_profit_margin_pct": "mean",
            "debt_to_equity": "mean"
        }
    )
    .round(2)
)

print()
print("Sector Dashboard")
print("=" * 50)
print(sector_summary)