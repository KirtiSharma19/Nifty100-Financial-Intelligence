from pathlib import Path

from src.services.ratio_engine import DatasetBuilder

engine = DatasetBuilder()

df = engine.build_dataset()

output = Path("exports")
output.mkdir(exist_ok=True)

latest = df[df["year"] == df["year"].max()]

latest.to_csv(
    output / "financial_report.csv",
    index=False
)

print("=" * 70)
print("FINANCIAL REPORT GENERATED")
print("=" * 70)
print(output / "financial_report.csv")