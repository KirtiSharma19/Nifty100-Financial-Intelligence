from src.analytics.cagr import CAGRCalculator
from src.utils.database import get_table
from src.analytics.ratios import calculate_ratios

pl = get_table("profitandloss")
bs = get_table("balancesheet")

merged = calculate_ratios(pl, bs)

print()

print("Revenue CAGR")

print(
    CAGRCalculator.calculate(
        100,
        180,
        5
    )
)

print()

print("PAT CAGR")

print(
    CAGRCalculator.calculate(
        50,
        120,
        5
    )
)

print()

print("Zero Base")

print(
    CAGRCalculator.calculate(
        0,
        120,
        5
    )
)
print()

print(
    merged[
        [
            "company_id",
            "year",
            "sales",
            "revenue_cagr_5yr"
        ]
    ].head(20)
)