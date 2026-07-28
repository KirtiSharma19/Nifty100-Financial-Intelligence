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
            "net_profit_margin_pct",
            "operating_profit_margin_pct",
            "roe_pct",
            "debt_to_equity"
        ]
    ].head(10)
)