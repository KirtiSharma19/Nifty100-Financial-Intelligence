from pathlib import Path

import matplotlib.pyplot as plt

from src.services.ratio_engine import DatasetBuilder

engine = DatasetBuilder()

df = engine.build_dataset()

latest = df[df["year"] == df["year"].max()]

top10 = latest.sort_values("quality_score", ascending=False).head(10)

Path("exports/charts").mkdir(parents=True, exist_ok=True)

plt.figure(figsize=(10, 5))

plt.bar(top10["company_name"], top10["quality_score"])

plt.xticks(rotation=45, ha="right")

plt.ylabel("Quality Score")

plt.title("Top 10 Companies")

plt.tight_layout()

plt.savefig("exports/charts/top10_quality_score.png")

plt.close()

print("Chart Generated Successfully.")
