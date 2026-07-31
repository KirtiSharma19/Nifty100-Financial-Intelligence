import pandas as pd

from src.services.ratio_engine import DatasetBuilder


class ScreenerEngine:

    def __init__(self):

        engine = DatasetBuilder()

        self.df = engine.build_dataset()

        # Latest year only
        self.df["year"] = (
            self.df["year"]
            .astype(str)
            .str.extract(r"(\d{4})")[0]
            .astype(int)
        )

        latest_year = self.df["year"].max()

        self.df = self.df[
            self.df["year"] == latest_year
        ].copy()

    # -------------------------------------------------
    # Generic Filter
    # -------------------------------------------------

    def screen(
        self,
        roe_min=None,
        debt_max=None,
        pe_max=None,
        pb_max=None,
        market_cap_min=None,
        dividend_min=None,
        revenue_cagr_min=None,
        pat_cagr_min=None,
        free_cash_flow_min=None,
        quality_min=None,
    ):

        df = self.df.copy()

        if roe_min is not None:
            df = df[
                df["return_on_equity_pct"] >= roe_min
            ]

        if debt_max is not None:
            df = df[
                df["debt_to_equity"] <= debt_max
            ]

        if pe_max is not None and "pe_ratio" in df.columns:
            df = df[
                df["pe_ratio"] <= pe_max
            ]

        if pb_max is not None and "pb_ratio" in df.columns:
            df = df[
                df["pb_ratio"] <= pb_max
            ]

        if market_cap_min is not None and "market_cap_crore" in df.columns:
            df = df[
                df["market_cap_crore"] >= market_cap_min
            ]

        if dividend_min is not None and "dividend_yield_pct" in df.columns:
            df = df[
                df["dividend_yield_pct"] >= dividend_min
            ]

        if revenue_cagr_min is not None and "sales_cagr" in df.columns:
            df = df[
                df["sales_cagr"] >= revenue_cagr_min
            ]

        if pat_cagr_min is not None and "pat_cagr" in df.columns:
            df = df[
                df["pat_cagr"] >= pat_cagr_min
            ]

        if free_cash_flow_min is not None:
            df = df[
                df["free_cash_flow_cr"] >= free_cash_flow_min
            ]

        if quality_min is not None:
            df = df[
                df["composite_score"] >= quality_min
            ]

        return df.sort_values(
            "composite_score",
            ascending=False
        ).reset_index(drop=True)

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
        df,
        filename="exports/screener_output.csv"
    ):

        df.to_csv(
            filename,
            index=False
        )

        print()
        print("=" * 60)
        print("Screener Exported Successfully")
        print(filename)
        print("=" * 60)

    # -------------------------------------------------
    # Summary
    # -------------------------------------------------

    def summary(self, df):

        print()
        print("=" * 60)
        print("SCREENER SUMMARY")
        print("=" * 60)

        print("Companies :", len(df))

        if len(df) == 0:
            return

        print()

        print(
            df[
                [
                    "company_name",
                    "broad_sector",
                    "composite_score",
                    "return_on_equity_pct",
                    "debt_to_equity",
                    "pe_ratio",
                    "pb_ratio",
                    "market_cap_crore",
                ]
            ]
        )

    def quality_compounder(self):

        return self.screen(
            roe_min=15,
            debt_max=1,
            free_cash_flow_min=0,
            quality_min=80
        )

    def value_pick(self):

        return self.screen(
            pe_max=20,
            pb_max=3,
            debt_max=2,
            dividend_min=1
        )

    def growth_accelerator(self):

        return self.screen(
            revenue_cagr_min=15,
            pat_cagr_min=20,
            debt_max=2
        )

    def dividend_champion(self):

        return self.screen(
            dividend_min=2,
            free_cash_flow_min=0
        )

    def debt_free_bluechip(self):

        return self.screen(
            debt_max=0,
            roe_min=12,
            market_cap_min=5000
        )

    def turnaround_watch(self):

        return self.screen(
            revenue_cagr_min=10,
            free_cash_flow_min=0
        )