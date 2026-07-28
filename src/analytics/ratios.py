"""
Financial Ratio Engine
"""

import pandas as pd


class RatioEngine:

    @staticmethod
    def safe_divide(a, b):

        if b in [0, None]:
            return None

        if pd.isna(b):
            return None

        return a / b

    @staticmethod
    def net_profit_margin(net_profit, sales):

        result = RatioEngine.safe_divide(
            net_profit,
            sales
        )

        if result is None:
            return None

        return round(result * 100, 2)

    @staticmethod
    def operating_profit_margin(
        operating_profit,
        sales
    ):

        result = RatioEngine.safe_divide(
            operating_profit,
            sales
        )

        if result is None:
            return None

        return round(result * 100, 2)

    @staticmethod
    def debt_to_equity(
        borrowings,
        equity
    ):

        if borrowings == 0:
            return 0

        return RatioEngine.safe_divide(
            borrowings,
            equity
        )

    @staticmethod
    def return_on_equity(
        net_profit,
        equity
    ):

        result = RatioEngine.safe_divide(
            net_profit,
            equity
        )

        if result is None:
            return None

        return round(result * 100, 2)

def calculate_ratios(pl_df, bs_df):

    merged = pd.merge(
        pl_df,
        bs_df,
        on=["company_id", "year"],
        how="inner"
    )

    # Net Profit Margin
    merged["net_profit_margin_pct"] = (
        merged["net_profit"] / merged["sales"]
    ) * 100

    # agar sales 0 ho
    merged.loc[
        merged["sales"] == 0,
        "net_profit_margin_pct"
    ] = None

        # Operating Profit Margin
    merged["operating_profit_margin_pct"] = (
        merged["operating_profit"] / merged["sales"]
    ) * 100

    merged.loc[
        merged["sales"] == 0,
        "operating_profit_margin_pct"
    ] = None

    # Return On Equity
    merged["return_on_equity_pct"] = (
        merged["net_profit"] /
        (merged["equity_capital"] + merged["reserves"])
    ) * 100

    merged.loc[
        (merged["equity_capital"] + merged["reserves"]) <= 0,
        "return_on_equity_pct"
    ] = None

    # Debt To Equity
    merged["debt_to_equity"] = (
        merged["borrowings"] /
        (merged["equity_capital"] + merged["reserves"])
    )

    merged.loc[
        (merged["equity_capital"] + merged["reserves"]) <= 0,
        "debt_to_equity"
    ] = None

    merged.loc[
        merged["borrowings"] == 0,
        "debt_to_equity"
    ] = 0 

    # Return On Capital Employed (ROCE)
    capital_employed = (
        merged["equity_capital"] +
        merged["reserves"] +
        merged["borrowings"]
    )

    merged["roce_pct"] = (
        merged["operating_profit"] /
        capital_employed
    ) * 100

    merged.loc[
        capital_employed <= 0,
        "roce_pct"
    ] = None

    # Return On Assets (ROA)
    merged["roa_pct"] = (
        merged["net_profit"] /
        merged["total_assets"]
    ) * 100

    merged.loc[
        merged["total_assets"] <= 0,
        "roa_pct"
    ] = None

    # Interest Coverage Ratio
    merged["interest_coverage"] = (
        merged["operating_profit"] +
        merged["other_income"]
    ) / merged["interest"]

    merged.loc[
        merged["interest"] == 0,
        "interest_coverage"
    ] = None

    merged["icr_label"] = ""

    merged.loc[
        merged["interest"] == 0,
        "icr_label"
    ] = "Debt Free"

    # Asset Turnover
    merged["asset_turnover"] = (
        merged["sales"] /
        merged["total_assets"]
    )

    merged.loc[
        merged["total_assets"] <= 0,
        "asset_turnover"
    ] = None

    from src.analytics.cagr import CAGRCalculator

    merged = merged.sort_values(["company_id", "year"])

    merged["revenue_cagr_5yr"] = None

    for company in merged["company_id"].unique():

        company_data = merged[merged["company_id"] == company]

        if len(company_data) >= 5:

            start_sales = company_data.iloc[0]["sales"]
            end_sales = company_data.iloc[-1]["sales"]

            merged.loc[
                merged["company_id"] == company,
                "revenue_cagr_5yr"
            ] = CAGRCalculator.calculate(
                start_sales,
                end_sales,
                5
            )
    return merged

def calculate_all_ratios(pl, bs, cf):

    merged = pl.merge(
        bs,
        on=["company_id", "year"]
    )

    merged = merged.merge(
        cf,
        on=["company_id", "year"]
    )

    return merged
