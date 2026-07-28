from pathlib import Path

from src.utils.database import get_table
from src.analytics.ratios import (
    calculate_all_ratios,
    RatioEngine,
)
from src.analytics.cashflow_kpis import CashflowKPI
from src.analytics.company_score import CompanyScore


class DatasetBuilder:

    def build_dataset(self):

        # Load Tables
        pl = get_table("profitandloss")
        bs = get_table("balancesheet")
        cf = get_table("cashflow")
        companies = get_table("companies")
        sectors = get_table("sectors")

        # Merge Financial Statements
        merged = calculate_all_ratios(
            pl,
            bs,
            cf
        )

        # -----------------------------
        # Company Name
        # -----------------------------
        company_data = companies[
            [
                "id",
                "company_name"
            ]
        ].rename(
            columns={
                "id": "company_id"
            }
        )

        merged = merged.merge(
            company_data,
            on="company_id",
            how="left"
        )

        # -----------------------------
        # Sector Info
        # -----------------------------
        sector_data = sectors[
            [
                "company_id",
                "broad_sector",
                "sub_sector"
            ]
        ]

        merged = merged.merge(
            sector_data,
            on="company_id",
            how="left"
        )

        # -----------------------------
        # Ratios
        # -----------------------------

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

        merged["return_on_equity_pct"] = merged.apply(
            lambda x: RatioEngine.return_on_equity(
                x["net_profit"],
                x["equity_capital"] + x["reserves"]
            ),
            axis=1
        )

        # -----------------------------
        # Cashflow KPIs
        # -----------------------------

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

        merged["cash_from_operations_cr"] = (
            merged["operating_activity"]
        )

        # -----------------------------
        # Quality Score
        # -----------------------------

        merged["quality_score"] = merged.apply(
            lambda x: CompanyScore.score(
                x["return_on_equity_pct"],
                x["debt_to_equity"],
                x["net_profit_margin_pct"]
            ),
            axis=1
        )

        # -----------------------------
        # Edge Case Log
        # -----------------------------

        self.log_edge_cases(merged)

        return merged

    def log_edge_cases(self, merged):

        financial_companies = {
            "AXISBANK",
            "BAJAJFINSV",
            "BAJAJHLDNG",
            "BAJFINANCE",
            "BANKBARODA",
            "CANBK",
            "CHOLAFIN",
            "HDFCBANK",
            "HDFCLIFE",
            "ICICIBANK",
            "ICICIGI",
            "ICICIPRULI",
            "INDUSINDBK",
            "IRFC",
            "JIOFIN",
            "KOTAKBANK",
            "LICI",
            "PFC",
            "PNB",
            "RECLTD",
            "SBILIFE",
            "SBIN",
            "SHRIRAMFIN"
        }

        log_file = Path(
            "output/ratio_edge_cases.log"
        )

        with open(
            log_file,
            "w",
            encoding="utf-8"
        ) as file:

            for _, row in merged.iterrows():

                company = row["company_id"]

                if company in financial_companies:
                    continue

                debt = row["debt_to_equity"]

                if debt is None:
                    continue

                if debt > 5:

                    file.write(
                        f"{company} | "
                        f"{row['year']} | "
                        f"High Debt To Equity : "
                        f"{debt:.2f}\n"
                    )

        print()
        print("Edge Case Log Generated.")