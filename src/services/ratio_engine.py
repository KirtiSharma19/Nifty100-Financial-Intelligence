from pathlib import Path

import pandas as pd

from src.analytics.company_score import CompanyScore
from src.analytics.composite_score import CompositeScore
from src.analytics.ratios import (
    RatioEngine,
    calculate_all_ratios,
)
from src.utils.database import get_table


class DatasetBuilder:

    # ============================================================
    # HELPER: REMOVE DUPLICATES FROM COMPANY TABLE
    # ============================================================

    @staticmethod
    def _prepare_company_data(companies):

        company_data = companies[["id", "company_name"]].copy()

        company_data = company_data.rename(columns={"id": "company_id"})

        # Keep only one company record per company_id
        company_data = company_data.drop_duplicates(subset=["company_id"], keep="first")

        return company_data

    # ============================================================
    # HELPER: REMOVE DUPLICATES FROM SECTOR TABLE
    # ============================================================

    @staticmethod
    def _prepare_sector_data(sectors):

        sector_data = sectors[["company_id", "broad_sector", "sub_sector"]].copy()

        # One sector record per company
        sector_data = sector_data.drop_duplicates(subset=["company_id"], keep="first")

        return sector_data

    # ============================================================
    # HELPER: REMOVE DUPLICATES FROM MARKET DATA
    # ============================================================

    @staticmethod
    def _prepare_market_data(market):

        market = market.copy()

        # Clean year
        market["year"] = market["year"].astype(str).str.extract(r"(\d{4})")[0]

        market["year"] = pd.to_numeric(market["year"], errors="coerce")

        # Remove rows where year could not be converted
        market = market.dropna(subset=["year"])

        market["year"] = market["year"].astype(int)

        required_columns = [
            "company_id",
            "year",
            "market_cap_crore",
            "enterprise_value_crore",
            "pe_ratio",
            "pb_ratio",
            "ev_ebitda",
            "dividend_yield_pct",
        ]

        market = market[required_columns].copy()

        # --------------------------------------------------------
        # IMPORTANT:
        # Market data must contain only ONE row
        # for each company + year.
        # --------------------------------------------------------

        market = market.drop_duplicates(subset=["company_id", "year"], keep="first")

        return market

    # ============================================================
    # HELPER: ENSURE ONE ROW PER COMPANY-YEAR
    # ============================================================

    @staticmethod
    def _remove_duplicate_company_years(df):

        df = df.copy()

        # Check duplicate company-year combinations
        duplicate_mask = df.duplicated(subset=["company_id", "year"], keep=False)

        duplicate_count = duplicate_mask.sum()

        if duplicate_count > 0:

            duplicate_groups = df.loc[
                duplicate_mask, ["company_id", "year"]
            ].drop_duplicates()

            print()
            print("=" * 60)
            print("DUPLICATE COMPANY-YEAR RECORDS FOUND")
            print("=" * 60)

            print("Duplicate rows:", duplicate_count)

            print("Duplicate company-year groups:", len(duplicate_groups))

            print()
            print(duplicate_groups.head(20).to_string(index=False))

            print()
            print("Keeping first record for each company-year.")

            # ----------------------------------------------------
            # Final safety layer.
            # ----------------------------------------------------

            df = df.drop_duplicates(
                subset=["company_id", "year"], keep="first"
            ).reset_index(drop=True)

        return df

    # ============================================================
    # MAIN DATASET BUILDER
    # ============================================================

    def build_dataset(self):

        print()
        print("=" * 60)
        print("LOADING DATA")
        print("=" * 60)

        # ========================================================
        # LOAD TABLES
        # ========================================================

        pl = get_table("profitandloss")
        bs = get_table("balancesheet")
        cf = get_table("cashflow")

        companies = get_table("companies")
        sectors = get_table("sectors")

        market = pd.read_excel("data/raw/market_cap.xlsx")

        # ========================================================
        # FINANCIAL STATEMENTS + RATIOS
        # ========================================================

        merged = calculate_all_ratios(pl, bs, cf)

        # --------------------------------------------------------
        # Clean year immediately
        # --------------------------------------------------------

        merged["year"] = merged["year"].astype(str).str.extract(r"(\d{4})")[0]

        merged["year"] = pd.to_numeric(merged["year"], errors="coerce")

        merged = merged.dropna(subset=["company_id", "year"])

        merged["year"] = merged["year"].astype(int)

        # ========================================================
        # CHECK FINANCIAL DATA DUPLICATES
        # ========================================================

        duplicate_financials = merged.duplicated(
            subset=["company_id", "year"], keep=False
        ).sum()

        print("Financial rows:", len(merged))

        print("Financial duplicate rows:", duplicate_financials)

        # ========================================================
        # COMPANY NAME
        # ========================================================

        company_data = self._prepare_company_data(companies)

        merged = merged.merge(
            company_data, on="company_id", how="left", validate="many_to_one"
        )

        # ========================================================
        # SECTOR INFO
        # ========================================================

        sector_data = self._prepare_sector_data(sectors)

        merged = merged.merge(
            sector_data, on="company_id", how="left", validate="many_to_one"
        )

        # ========================================================
        # MARKET VALUATION
        # ========================================================

        market = self._prepare_market_data(market)

        merged = merged.merge(
            market, on=["company_id", "year"], how="left", validate="many_to_one"
        )

        # ========================================================
        # REMOVE FINAL COMPANY-YEAR DUPLICATES
        # ========================================================

        merged = self._remove_duplicate_company_years(merged)

        # ========================================================
        # RATIOS
        # ========================================================

        print()
        print("=" * 60)
        print("CALCULATING RATIOS")
        print("=" * 60)

        merged["net_profit_margin_pct"] = merged.apply(
            lambda x: RatioEngine.net_profit_margin(x["net_profit"], x["sales"]), axis=1
        )

        merged["operating_profit_margin_pct"] = merged.apply(
            lambda x: RatioEngine.operating_profit_margin(
                x["operating_profit"], x["sales"]
            ),
            axis=1,
        )

        merged["debt_to_equity"] = merged.apply(
            lambda x: RatioEngine.debt_to_equity(
                x["borrowings"], x["equity_capital"] + x["reserves"]
            ),
            axis=1,
        )

        merged["return_on_equity_pct"] = merged.apply(
            lambda x: RatioEngine.return_on_equity(
                x["net_profit"], x["equity_capital"] + x["reserves"]
            ),
            axis=1,
        )

        # ========================================================
        # CASHFLOW KPIs
        # ========================================================

        print()
        print("=" * 60)
        print("CALCULATING CASHFLOW KPIs")
        print("=" * 60)

        merged["free_cash_flow_cr"] = (
            merged["operating_activity"] + merged["investing_activity"]
        )

        merged["capex_cr"] = (
            merged["investing_activity"].abs() / merged["sales"]
        ) * 100

        merged["cash_from_operations_cr"] = merged["operating_activity"]

        # ========================================================
        # QUALITY SCORE
        # ========================================================

        merged["quality_score"] = merged.apply(
            lambda x: CompanyScore.score(
                x["return_on_equity_pct"],
                x["debt_to_equity"],
                x["net_profit_margin_pct"],
            ),
            axis=1,
        )

        # ========================================================
        # COMPOSITE SCORE
        # ========================================================

        merged["composite_score"] = merged.apply(
            lambda x: CompositeScore.calculate(
                x["return_on_equity_pct"],
                x["net_profit_margin_pct"],
                x["free_cash_flow_cr"],
                x["debt_to_equity"],
                x["dividend_yield_pct"],
            ),
            axis=1,
        )

        # ========================================================
        # EDGE CASE LOG
        # ========================================================

        self.log_edge_cases(merged)

        # ========================================================
        # FINAL VALIDATION
        # ========================================================

        final_duplicates = merged.duplicated(subset=["company_id", "year"]).sum()

        print()
        print("=" * 60)
        print("FINAL DATASET CHECK")
        print("=" * 60)

        print("Rows:", len(merged))

        print("Companies:", merged["company_id"].nunique())

        print("Duplicate company-year rows:", final_duplicates)

        if final_duplicates != 0:

            raise ValueError(
                "Dataset still contains duplicate " "company-year records."
            )

        print()
        print("DatasetBuilder completed successfully.")

        return merged

    # ============================================================
    # EDGE CASE LOG
    # ============================================================

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
            "SHRIRAMFIN",
        }

        log_file = Path("output/ratio_edge_cases.log")

        # Make sure output folder exists
        log_file.parent.mkdir(parents=True, exist_ok=True)

        with open(log_file, "w", encoding="utf-8") as file:

            for _, row in merged.iterrows():

                company = row["company_id"]

                if company in financial_companies:
                    continue

                debt = row["debt_to_equity"]

                if pd.isna(debt):
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
