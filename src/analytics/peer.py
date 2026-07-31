import pandas as pd

from src.services.ratio_engine import DatasetBuilder


class PeerEngine:

    def __init__(self):

        engine = DatasetBuilder()

        self.df = engine.build_dataset()

        # -----------------------------
        # Latest Year Only
        # -----------------------------

        self.df["year"] = (
            self.df["year"]
            .astype(str)
            .str.extract(r"(\d{4})")[0]
            .astype(int)
        )

        latest = self.df["year"].max()

        self.df = self.df[
            self.df["year"] == latest
        ].copy()

        # -----------------------------
        # Peer Groups
        # -----------------------------

        peer = pd.read_excel(
            "data/raw/peer_groups.xlsx"
        )

        peer = peer.rename(
            columns={
                "peer_group_name": "peer_group"
            }
        )

        self.df = self.df.merge(
            peer[
                [
                    "company_id",
                    "peer_group"
                ]
            ],
            on="company_id",
            how="left"
        )

    # ---------------------------------------------------

    def calculate_percentiles(self):

        metrics = [

            "return_on_equity_pct",

            "net_profit_margin_pct",

            "debt_to_equity",

            "free_cash_flow_cr",

            "composite_score"

        ]

        higher_is_better = {

            "return_on_equity_pct": True,

            "net_profit_margin_pct": True,

            "free_cash_flow_cr": True,

            "composite_score": True,

            "debt_to_equity": False

        }

        for metric in metrics:

            if higher_is_better[metric]:

                self.df[
                    metric + "_percentile"
                ] = (
                    self.df
                    .groupby("peer_group")[metric]
                    .rank(
                        pct=True,
                        ascending=True
                    ) * 100
                )

            else:

                self.df[
                    metric + "_percentile"
                ] = (
                    self.df
                    .groupby("peer_group")[metric]
                    .rank(
                        pct=True,
                        ascending=False
                    ) * 100
                )

        return self.df

    # ---------------------------------------------------

    def export(self):

        cols = [

            "company_name",

            "peer_group",

            "return_on_equity_pct_percentile",

            "net_profit_margin_pct_percentile",

            "debt_to_equity_percentile",

            "free_cash_flow_cr_percentile",

            "composite_score_percentile"

        ]

        self.df[
            cols
        ].to_csv(

            "exports/peer_comparison.csv",

            index=False

        )

        print()

        print("=" * 70)

        print("Peer Comparison Saved")

        print("=" * 70)

        print("exports/peer_comparison.csv")

    # ---------------------------------------------------

    def summary(self):

        print()

        print("=" * 70)

        print("PEER RANKINGS")

        print("=" * 70)

        print(

            self.df[

                [

                    "company_name",

                    "peer_group",

                    "composite_score",

                    "composite_score_percentile"

                ]

            ].head(10)

        )