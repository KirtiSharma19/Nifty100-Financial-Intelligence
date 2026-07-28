from src.analytics.cagr import CAGRCalculator

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