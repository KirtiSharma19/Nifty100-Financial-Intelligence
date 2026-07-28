from src.services.ratio_engine import RatioEngine

engine = RatioEngine()

merged = engine.build_dataset()

print()

print("Merged Dataset")

print()

print(merged.shape)

print()

print(
    merged[
        [
            "company_id",
            "year",
            "net_profit_margin_pct",
            "operating_profit_margin_pct",
            "debt_to_equity",
            "free_cash_flow_cr"
        ]
    ].head(20)
)