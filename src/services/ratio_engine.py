from src.utils.database import get_table
from src.analytics.ratios import calculate_all_ratios


class RatioEngine:

    def build_dataset(self):

        pl = get_table("profitandloss")
        bs = get_table("balancesheet")
        cf = get_table("cashflow")
        from src.analytics.ratios import RatioEngine
        from src.analytics.cashflow_kpis import CashflowKPI

        merged = calculate_all_ratios(
            pl,
            bs,
            cf
        )
        merged["net_profit_margin_pct"] = merged.apply(
            lambda x: RatioEngine.net_profit_margin(
            x["net_profit"],
            x["sales"]
        ),
        axis=1
        )

        merged["operating_profit_margin_pct"] = merged.apply(
            lambda x: RatioEngine.operating_profit_margin(
            x["operating_profit"],
            x["sales"]
            ),
            axis=1
        )

        merged["debt_to_equity"] = merged.apply(
            lambda x: RatioEngine.debt_to_equity(
            x["borrowings"],
            x["equity_capital"] + x["reserves"]
            ),
            axis=1
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

        return merged