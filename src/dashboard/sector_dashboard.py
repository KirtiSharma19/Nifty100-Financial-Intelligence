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

import matplotlib.pyplot as plt

sector_summary = sector_summary.sort_values(
    "quality_score",
    ascending=False
)

plt.figure(figsize=(12,6))

plt.bar(
    sector_summary.index,
    sector_summary["quality_score"]
)

plt.xticks(rotation=45, ha="right")

plt.title("Sector Wise Quality Score")
plt.ylabel("Average Quality Score")

plt.tight_layout()

plt.savefig(
    "exports/charts/sector_quality_score.png"
)

plt.show()