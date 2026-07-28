from src.utils.database import get_table

ratios = get_table("financial_ratios")

print()

print(ratios.head())

print()

print("Rows :", len(ratios))

print()

print(ratios.columns.tolist())