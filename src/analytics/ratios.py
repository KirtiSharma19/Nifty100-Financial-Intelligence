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

    return merged