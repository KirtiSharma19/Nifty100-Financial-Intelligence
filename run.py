from src.utils.database import get_table
from src.analytics.ratios import calculate_ratios

pl = get_table("profitandloss")
bs = get_table("balancesheet")

merged = calculate_ratios(pl, bs)

print()

print(
    merged[
        [
            "company_id",
            "year",
            "roe_pct",
            "roce_pct",
            "roa_pct",
            "interest_coverage",
            "asset_turnover"
        ]
    ].head(10)
)