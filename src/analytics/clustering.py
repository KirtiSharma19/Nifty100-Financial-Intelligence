import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from src.services.ratio_engine import DatasetBuilder


# ============================================================
# CAGR HELPER
# ============================================================

def calculate_cagr(start_value, end_value, years):
    """
    Calculate CAGR in percentage.

    CAGR = ((End Value / Start Value)^(1 / Years) - 1) * 100

    CAGR is calculated only when both start and end values
    are positive.
    """

    if pd.isna(start_value) or pd.isna(end_value):
        return np.nan

    if years <= 0:
        return np.nan

    if start_value <= 0 or end_value <= 0:
        return np.nan

    try:
        cagr = (
            ((end_value / start_value) ** (1 / years)) - 1
        ) * 100

        return round(cagr, 2)

    except (ValueError, ZeroDivisionError, OverflowError):
        return np.nan


# ============================================================
# LOAD DATA
# ============================================================

print()
print("=" * 70)
print("LOADING DATA")
print("=" * 70)

engine = DatasetBuilder()

df = engine.build_dataset()

print("Rows loaded :", len(df))
print("Companies   :", df["company_id"].nunique())


# ============================================================
# CLEAN YEAR
# ============================================================

df["year"] = (
    df["year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
)

df["year"] = pd.to_numeric(
    df["year"],
    errors="coerce"
)

df = df.dropna(subset=["year"])

df["year"] = df["year"].astype(int)


# ============================================================
# SORT DATA
# ============================================================

df = df.sort_values(
    ["company_id", "year"]
).copy()


# ============================================================
# CALCULATE EXACT 5-YEAR CAGR FEATURES
# ============================================================

print()
print("=" * 70)
print("CALCULATING 5-YEAR CAGR FEATURES")
print("=" * 70)

df["revenue_cagr_5yr"] = np.nan
df["fcf_cagr_5yr"] = np.nan


for company in df["company_id"].dropna().unique():

    company_data = (
        df[df["company_id"] == company]
        .sort_values("year")
        .copy()
    )

    # Latest available year for this company
    company_latest_year = company_data["year"].max()

    # Exactly 5 years before latest year
    start_year = company_latest_year - 5

    start_data = company_data[
        company_data["year"] == start_year
    ]

    end_data = company_data[
        company_data["year"] == company_latest_year
    ]

    # We need both years
    if start_data.empty or end_data.empty:
        continue

    start_row = start_data.iloc[0]
    end_row = end_data.iloc[0]

    start_sales = start_row["sales"]
    end_sales = end_row["sales"]

    start_fcf = start_row["free_cash_flow_cr"]
    end_fcf = end_row["free_cash_flow_cr"]

    # --------------------------------------------------------
    # Revenue / Sales CAGR
    # --------------------------------------------------------

    revenue_cagr = calculate_cagr(
        start_sales,
        end_sales,
        5
    )

    # --------------------------------------------------------
    # Free Cash Flow CAGR
    # --------------------------------------------------------

    fcf_cagr = calculate_cagr(
        start_fcf,
        end_fcf,
        5
    )

    # Assign values to all rows belonging to this company
    df.loc[
        df["company_id"] == company,
        "revenue_cagr_5yr"
    ] = revenue_cagr

    df.loc[
        df["company_id"] == company,
        "fcf_cagr_5yr"
    ] = fcf_cagr


# ============================================================
# LATEST YEAR DATA
# ============================================================

latest_year = df["year"].max()

latest = df[
    df["year"] == latest_year
].copy()


print()
print("=" * 70)
print("LATEST YEAR DATA")
print("=" * 70)

print("Latest Year :", latest_year)
print("Companies   :", latest["company_id"].nunique())


# ============================================================
# CAGR FEATURE CHECK
# ============================================================

print()
print("=" * 70)
print("CAGR FEATURES CHECK")
print("=" * 70)

print(
    latest[
        [
            "company_id",
            "company_name",
            "revenue_cagr_5yr",
            "fcf_cagr_5yr"
        ]
    ].head(10)
)


print()
print(
    "Missing Revenue CAGR:",
    latest["revenue_cagr_5yr"].isna().sum()
)

print(
    "Missing FCF CAGR:",
    latest["fcf_cagr_5yr"].isna().sum()
)


# ============================================================
# REQUIRED FEATURES
# ============================================================

features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "fcf_cagr_5yr",
    "operating_profit_margin_pct",
]


# ============================================================
# CHECK REQUIRED FEATURES
# ============================================================

missing_features = [
    col
    for col in features
    if col not in latest.columns
]

if missing_features:

    print()
    print("ERROR: MISSING FEATURES")
    print(missing_features)

    print()
    print("Available columns:")
    print(latest.columns.tolist())

    raise SystemExit


# ============================================================
# CONVERT FEATURES TO NUMERIC
# ============================================================

for col in features:

    latest[col] = pd.to_numeric(
        latest[col],
        errors="coerce"
    )


# ============================================================
# SECTOR MEDIAN IMPUTATION
# ============================================================

print()
print("=" * 70)
print("SECTOR MEDIAN IMPUTATION")
print("=" * 70)

for col in features:

    # First: fill missing value using sector median
    latest[col] = (
        latest
        .groupby("broad_sector")[col]
        .transform(
            lambda x: x.fillna(x.median())
        )
    )

    # Second: if sector median is also missing,
    # use global median
    global_median = latest[col].median()

    if pd.isna(global_median):

        print(
            f"WARNING: {col} has no valid values."
        )

    else:

        latest[col] = latest[col].fillna(
            global_median
        )


# ============================================================
# FINAL NaN CHECK
# ============================================================

remaining_missing = (
    latest[features]
    .isna()
    .sum()
)

print()
print("Remaining missing values:")
print(remaining_missing)


# If any feature is completely unavailable,
# K-Means cannot be performed reliably.

if remaining_missing.sum() > 0:

    print()
    print("ERROR: Missing values remain after imputation.")
    print("K-Means cannot continue safely.")

    raise SystemExit


# ============================================================
# FEATURE MATRIX
# ============================================================

X = latest[
    features
].copy()


# ============================================================
# STANDARD SCALING
# ============================================================

print()
print("=" * 70)
print("STANDARD SCALING")
print("=" * 70)

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# ============================================================
# CREATE OUTPUT DIRECTORIES
# ============================================================

os.makedirs(
    "reports",
    exist_ok=True
)

os.makedirs(
    "output",
    exist_ok=True
)


# ============================================================
# ELBOW METHOD
# ============================================================

print()
print("=" * 70)
print("ELBOW METHOD")
print("=" * 70)

inertias = []

for k in range(2, 11):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(X_scaled)

    inertias.append(
        model.inertia_
    )


# ============================================================
# ELBOW PLOT
# ============================================================

plt.figure(
    figsize=(9, 6)
)

plt.plot(
    range(2, 11),
    inertias,
    marker="o"
)

plt.xlabel(
    "Number of Clusters (k)"
)

plt.ylabel(
    "Inertia"
)

plt.title(
    "K-Means Elbow Plot"
)

plt.xticks(
    range(2, 11)
)

plt.grid(
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "reports/elbow_plot.png",
    dpi=150
)

plt.close()

print(
    "Saved: reports/elbow_plot.png"
)


# ============================================================
# FINAL K-MEANS MODEL
# ============================================================

print()
print("=" * 70)
print("RUNNING FINAL K-MEANS")
print("=" * 70)

kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

latest["cluster_id"] = (
    kmeans.fit_predict(X_scaled)
)


# ============================================================
# CLUSTER CENTROIDS
# ============================================================

centroids = pd.DataFrame(
    scaler.inverse_transform(
        kmeans.cluster_centers_
    ),
    columns=features
)

centroids.index.name = "cluster_id"


print()
print("=" * 70)
print("CLUSTER PROFILES")
print("=" * 70)

print(
    centroids.round(2)
)


# ============================================================
# CLUSTER SIZE
# ============================================================

print()
print("=" * 70)
print("CLUSTER SIZE")
print("=" * 70)

cluster_sizes = (
    latest["cluster_id"]
    .value_counts()
    .sort_index()
)

print(cluster_sizes)


# ============================================================
# SAVE CLUSTER LABELS
# ============================================================

cluster_labels = latest[
    [
        "company_id",
        "company_name",
        "broad_sector",
        "cluster_id"
    ]
].copy()


cluster_labels.to_csv(
    "output/cluster_labels.csv",
    index=False
)


# ============================================================
# SAVE FULL CLUSTER DATA
# ============================================================

cluster_output = latest[
    [
        "company_id",
        "company_name",
        "broad_sector",
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "fcf_cagr_5yr",
        "operating_profit_margin_pct",
        "cluster_id"
    ]
].copy()


cluster_output.to_csv(
    "output/cluster_analysis.csv",
    index=False
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 70)
print("CLUSTERING COMPLETED")
print("=" * 70)

print(
    "Clusters  :",
    latest["cluster_id"].nunique()
)

print(
    "Companies :",
    latest["company_id"].nunique()
)

print()
print("Saved files:")
print("1. reports/elbow_plot.png")
print("2. output/cluster_labels.csv")
print("3. output/cluster_analysis.csv")

print()
print("=" * 70)
print("DONE")
print("=" * 70)