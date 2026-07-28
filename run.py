from src.utils.database import get_table
from src.analytics.cashflow_kpis import CashflowKPI
from src.analytics.ratios import calculate_all_ratios

pl = get_table("profitandloss")
bs = get_table("balancesheet")
cf = get_table("cashflow")

merged = pl.merge(
    cf,
    on=["company_id", "year"]
)
merged = calculate_all_ratios(
    pl,
    bs,
    cf
)

merged["free_cash_flow_cr"] = merged.apply(
    lambda x: CashflowKPI.free_cash_flow(
        x["operating_activity"],
        x["investing_activity"]
    ),
    axis=1
)

merged["capex_cr"] = merged.apply(
    lambda x: CashflowKPI.capex_intensity(
        x["investing_activity"],
        x["sales"]
    ),
    axis=1
)

merged["cash_from_operations_cr"] = merged["operating_activity"]

print(
    merged[
        [
            "company_id",
            "year",
            "free_cash_flow_cr",
            "capex_cr",
            "cash_from_operations_cr"
        ]
    ].head(20)
)
from src.etl.database_loader import DatabaseLoader
print(merged.columns.tolist())
loader = DatabaseLoader()

loader.save_financial_ratios(merged)
print()

print(merged.shape)

print()

print(merged.head())