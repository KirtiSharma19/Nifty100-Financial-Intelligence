import streamlit as st
import matplotlib.pyplot as plt

from src.services.ratio_engine import DatasetBuilder

def show_sector_dashboard():
# -------------------------------------------------------
# Load Dataset
# -------------------------------------------------------

    engine = DatasetBuilder()

    df = engine.build_dataset()


# -------------------------------------------------------
# Clean Year
# -------------------------------------------------------

    df["year"] = (
    df["year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
    .astype(int)
    )

    latest_year = df["year"].max()

    latest = df[df["year"] == latest_year]


# -------------------------------------------------------
# Page Title
# -------------------------------------------------------

    st.title("Sector Dashboard")


# -------------------------------------------------------
# Sector Dropdown
# -------------------------------------------------------

    sector = st.selectbox(
        "Select Sector",
            sorted(
                latest["broad_sector"]
                .dropna()
                .unique()
            )
    )

    sector_df = latest[
        latest["broad_sector"] == sector
    ]


# -------------------------------------------------------
# Metrics
# -------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Average Quality Score",
            round(
            sector_df["quality_score"].mean(),
            2
        )
    )

    col2.metric(
        "Average ROE %",
            round(
            sector_df["return_on_equity_pct"].mean(),
            2
        )
    )

    col3.metric(
        "Average Net Margin %",
            round(
            sector_df["net_profit_margin_pct"].mean(),
            2
        )
    )

    col4.metric(
        "Companies",
        sector_df["company_name"].nunique()
    )


# -------------------------------------------------------
# Top Companies
# -------------------------------------------------------

    st.subheader("Top Companies")

    top_companies = sector_df.sort_values(
        "quality_score",
        ascending=False
    )

    st.dataframe(
        top_companies[
        [
            "company_name",
            "quality_score",
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "free_cash_flow_cr"
        ]
    ],
    use_container_width=True
    )


# -------------------------------------------------------
# Quality Score Chart
# -------------------------------------------------------

    st.subheader("Top 10 Quality Score")

    top10 = top_companies.head(10)

    fig, ax = plt.subplots(figsize=(10,5))

    ax.bar(
        top10["company_name"],
        top10["quality_score"]
    )

    ax.set_ylabel("Quality Score")

    ax.set_xlabel("Company")

    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()

    st.pyplot(fig)


# -------------------------------------------------------
# ROE Chart
# -------------------------------------------------------

    st.subheader("ROE Comparison")

    fig, ax = plt.subplots(figsize=(10,5))

    ax.bar(
        top10["company_name"],
        top10["return_on_equity_pct"]
    )

    ax.set_ylabel("ROE %")

    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()

    st.pyplot(fig)


# -------------------------------------------------------
# Net Profit Margin Chart
# -------------------------------------------------------

    st.subheader("Net Profit Margin")

    fig, ax = plt.subplots(figsize=(10,5))

    ax.bar(
        top10["company_name"],
        top10["net_profit_margin_pct"]
    )

    ax.set_ylabel("Margin %")

    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()

    st.pyplot(fig)

# -------------------------------------------------------
# Debt to Equity Chart
# -------------------------------------------------------

    st.subheader("Debt to Equity")

    fig, ax = plt.subplots(figsize=(10,5))

    ax.bar(
        top10["company_name"],
        top10["debt_to_equity"]
    )

    ax.set_ylabel("Debt / Equity")

    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()

    st.pyplot(fig)

# -------------------------------------------------------
# Free Cash Flow Chart
# -------------------------------------------------------

    st.subheader("Free Cash Flow")

    fig, ax = plt.subplots(figsize=(10,5))

    ax.bar(
        top10["company_name"],
        top10["free_cash_flow_cr"]
    )

    ax.set_ylabel("Cash Flow (Cr)")

    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()

    st.pyplot(fig)