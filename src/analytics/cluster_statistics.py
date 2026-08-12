from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


INPUT_FILE = "output/cluster_analysis.csv"

FEATURES = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "fcf_cagr_5yr",
    "operating_profit_margin_pct",
]

# 10 KPIs required for correlation + portfolio statistics.
KPI_CANDIDATES = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "fcf_cagr_5yr",
    "operating_profit_margin_pct",
    "net_profit_margin_pct",
    "free_cash_flow_cr",
    "cash_from_operations_cr",
    "capex_cr",
    "quality_score",
]

CLUSTER_NAMES = {
    0: "Balanced Quality Companies",
    1: "Leveraged Turnaround",
    2: "Extreme-ROE Outliers",
    3: "High-Margin Leaders",
    4: "Cashflow Growth Leader",
}


def load_data():
    """Load the final clustering dataset."""
    return pd.read_csv(INPUT_FILE)


def create_cluster_profiles(df):
    """Create mean and median financial profiles for every cluster."""

    profiles = (
        df.groupby("cluster_id")[FEATURES]
        .agg(["mean", "median"])
        .round(2)
    )

    Path("output").mkdir(exist_ok=True)

    # Flatten MultiIndex columns
    profiles.columns = [
        f"{feature}_{stat}"
        for feature, stat in profiles.columns
    ]

    profiles.insert(
        0,
        "cluster_name",
        profiles.index.map(CLUSTER_NAMES)
    )

    profiles.to_csv("output/cluster_profiles.csv")

    print("\nCLUSTER PROFILES")
    print("=" * 70)
    print(profiles.to_string())

    return profiles


def create_cluster_labels(df):
    """Create company-level cluster labels."""

    labels = df[
        ["company_id", "company_name", "cluster_id"]
    ].copy()

    labels["cluster_name"] = labels["cluster_id"].map(CLUSTER_NAMES)

    labels["distance_from_centroid"] = np.nan

    labels = labels[
        [
            "company_id",
            "company_name",
            "cluster_id",
            "cluster_name",
            "distance_from_centroid",
        ]
    ]

    labels.to_csv(
        "output/cluster_labels.csv",
        index=False
    )

    print("\nCLUSTER LABELS")
    print("=" * 70)
    print("Companies:", len(labels))
    print(
        "Missing cluster IDs:",
        labels["cluster_id"].isna().sum()
    )

    return labels


def create_correlation_heatmap(df):
    """Create Pearson correlation heatmap for the 10 KPIs."""

    available = [
        col for col in KPI_CANDIDATES
        if col in df.columns
    ]

    print("\nKPI COLUMNS AVAILABLE")
    print(available)

    if len(available) < 10:
        print(
            f"WARNING: Only {len(available)} of 10 KPI columns "
            "are currently available."
        )

    correlation = df[available].corr(method="pearson")

    Path("reports").mkdir(exist_ok=True)

    plt.figure(figsize=(14, 10))

    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        square=True,
        linewidths=0.5
    )

    plt.title(
        "Pearson Correlation Matrix - Financial KPIs"
    )

    plt.tight_layout()

    plt.savefig(
        "reports/correlation_heatmap.png",
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

    print(
        "Saved: reports/correlation_heatmap.png"
    )


def create_outlier_report(df):
    """Detect sector-wise KPI outliers using absolute Z-score > 3."""

    available = [
        col for col in FEATURES
        if col in df.columns
    ]

    outliers = []

    for sector, group in df.groupby("broad_sector"):

        for metric in available:

            values = pd.to_numeric(
                group[metric],
                errors="coerce"
            )

            mean = values.mean()
            std = values.std(ddof=0)

            if pd.isna(std) or std == 0:
                continue

            z_scores = (values - mean) / std

            mask = z_scores.abs() > 3

            for idx in group.index[mask]:

                outliers.append({
                    "company_id": df.loc[idx, "company_id"],
                    "company_name": df.loc[idx, "company_name"],
                    "broad_sector": sector,
                    "metric": metric,
                    "value": df.loc[idx, metric],
                    "z_score": z_scores.loc[idx],
                })

    outlier_df = pd.DataFrame(outliers)

    if not outlier_df.empty:
        outlier_df = outlier_df.sort_values(
            "z_score",
            key=lambda x: x.abs(),
            ascending=False
        )

    outlier_df.to_csv(
        "output/outlier_report.csv",
        index=False
    )

    print("\nOUTLIER REPORT")
    print("=" * 70)
    print(
        "Outliers found:",
        len(outlier_df)
    )
    print(
        "Saved: output/outlier_report.csv"
    )

    if not outlier_df.empty:
        print("\nTop outliers:")
        print(
            outlier_df.head(10).to_string(index=False)
        )


def create_portfolio_stats(df):
    """Generate P10-P90, mean and standard deviation for KPIs."""

    available = [
        col for col in KPI_CANDIDATES
        if col in df.columns
    ]

    rows = []

    for metric in available:

        values = pd.to_numeric(
            df[metric],
            errors="coerce"
        ).dropna()

        rows.append({
            "kpi": metric,
            "P10": values.quantile(0.10),
            "P25": values.quantile(0.25),
            "P50": values.quantile(0.50),
            "P75": values.quantile(0.75),
            "P90": values.quantile(0.90),
            "Mean": values.mean(),
            "Std": values.std(),
        })

    stats = pd.DataFrame(rows).round(4)

    stats.to_csv(
        "output/portfolio_stats.csv",
        index=False
    )

    print("\nPORTFOLIO STATISTICS")
    print("=" * 70)
    print(stats.to_string(index=False))

    print(
        "\nSaved: output/portfolio_stats.csv"
    )


def main():

    print("=" * 70)
    print("SPRINT 6 - DAY 37 STATISTICS")
    print("=" * 70)

    df = load_data()

    print("\nRows:", len(df))
    print("Companies:", df["company_id"].nunique())

    create_cluster_profiles(df)

    create_cluster_labels(df)

    create_correlation_heatmap(df)

    create_outlier_report(df)

    create_portfolio_stats(df)

    print("\n" + "=" * 70)
    print("DAY 37 COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()