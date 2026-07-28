from src.services.ratio_engine import DatasetBuilder

engine = DatasetBuilder()

merged = engine.build_dataset()

print(
    merged[
        [
            "company_name",
            "broad_sector",
            "quality_score"
        ]
    ].head(20)
)