from src.utils.database import get_table
from src.analytics.ratios import calculate_all_ratios
from pathlib import Path


class RatioEngine:

    def build_dataset(self):

        pl = get_table("profitandloss")
        bs = get_table("balancesheet")
        cf = get_table("cashflow")

        from src.analytics.ratios import RatioEngine
        from src.analytics.cashflow_kpis import CashflowKPI

        merged = calculate_all_ratios(pl, bs, cf)

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

        self.log_edge_cases(merged)

        return merged

    def log_edge_cases(self, merged):

        companies = get_table("companies")
        sectors = get_table("sectors")

        sector_df = companies.merge(
            sectors,
            left_on="id",
            right_on="company_id",
            how="inner"
        )

        financial_companies = set(
            sector_df.loc[
                sector_df["broad_sector"] == "Financials",
                "id_x"
            ].astype(str).str.upper()
        )

        print("\nFinancial Companies Found:")
        print(sorted(financial_companies))

        log_file = Path("output/ratio_edge_cases.log")

        with open(log_file, "w", encoding="utf-8") as file:

            for _, row in merged.iterrows():

                company = str(row["company_id"]).upper()

                if company in financial_companies:
                    continue

                debt = row["debt_to_equity"]

                if debt is None:
                    continue

                if debt > 5:
                    file.write(
                        f"{company} | {row['year']} | High Debt To Equity : {debt:.2f}\n"
                    )

        print("\nEdge Case Log Generated.")
        print(financial_companies)