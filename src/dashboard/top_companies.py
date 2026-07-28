from src.services.ratio_engine import DatasetBuilder

engine = DatasetBuilder()

df = engine.build_dataset()

latest_year = df["year"].max()

latest = df[df["year"] == latest_year]

top10 = (
    latest[
        [
            "company_name",
            "broad_sector",
            "quality_score",
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
        ]
    ]
    .sort_values(
        "quality_score",
        ascending=False
    )
    .head(10)
)

print()
print("=" * 90)
print("TOP 10 QUALITY COMPANIES")
print("=" * 90)
print(top10)