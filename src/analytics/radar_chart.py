import os

import matplotlib.pyplot as plt
import numpy as np

from src.services.ratio_engine import DatasetBuilder


class RadarChartEngine:

    def __init__(self):

        engine = DatasetBuilder()

        self.df = engine.build_dataset()

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

        os.makedirs(
            "exports/radar_charts",
            exist_ok=True
        )

    # ---------------------------------------------------------

    def generate(self):

        metrics = [

            "return_on_equity_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "composite_score",
            "pe_ratio",
            "pb_ratio",
            "dividend_yield_pct"

        ]

        labels = [

            "ROE",
            "Net Margin",
            "Debt/Equity",
            "FCF",
            "Composite",
            "PE",
            "PB",
            "Dividend"

        ]

        for _, row in self.df.iterrows():

            values = []

            for metric in metrics:

                value = row.get(metric)

                if value is None:
                    value = 0

                try:
                    value = float(value)
                except Exception:
                    value = 0

                values.append(value)

            max_value = max(values)

            if max_value == 0:
                continue

            values = [v / max_value for v in values]

            values += values[:1]

            angles = np.linspace(
                0,
                2 * np.pi,
                len(labels),
                endpoint=False
            ).tolist()

            angles += angles[:1]

            plt.figure(figsize=(7, 7))

            ax = plt.subplot(
                111,
                polar=True
            )

            ax.plot(
                angles,
                values,
                linewidth=2
            )

            ax.fill(
                angles,
                values,
                alpha=0.25
            )

            ax.set_xticks(angles[:-1])

            ax.set_xticklabels(labels)

            ax.set_title(
                row["company_name"],
                fontsize=12
            )

            filename = (
                row["company_id"]
                .replace("/", "_")
                .replace("\\", "_")
            )

            plt.tight_layout()

            plt.savefig(
                f"exports/radar_charts/{filename}.png"
            )

            plt.close()

        print()

        print("=" * 70)
        print("Radar Charts Generated")
        print("=" * 70)
        print("exports/radar_charts/")