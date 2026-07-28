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
            "sales",
            "net_profit",
            "net_profit_margin_pct"
        ]
    ].head(10)
)