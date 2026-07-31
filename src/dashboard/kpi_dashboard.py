import streamlit as st

from src.services.ratio_engine import DatasetBuilder

engine = DatasetBuilder()
df = engine.build_dataset()


def show_kpi_dashboard():

    st.title("KPI Dashboard")

    latest_year = df["year"].max()

    latest = df[df["year"] == latest_year]

    # -----------------------------
    # KPI Cards
    # -----------------------------

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Highest Quality",
        round(latest["quality_score"].max(), 2)
    )

    c2.metric(
        "Highest ROE %",
        round(latest["return_on_equity_pct"].max(), 2)
    )

    c3.metric(
        "Highest Margin %",
        round(latest["net_profit_margin_pct"].max(), 2)
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "Lowest Debt/Equity",
        round(latest["debt_to_equity"].min(), 2)
    )

    c5.metric(
        "Average Quality",
        round(latest["quality_score"].mean(), 2)
    )

    c6.metric(
        "Companies",
        latest["company_name"].nunique()
    )

    st.divider()

    # -----------------------------
    # Top Quality
    # -----------------------------

    st.subheader("Top 10 Quality Companies")

    top_quality = (
        latest[
            [
                "company_name",
                "quality_score"
            ]
        ]
        .sort_values(
            "quality_score",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_quality,
        use_container_width=True
    )

    st.bar_chart(
        top_quality.set_index("company_name")
    )

    # -----------------------------
    # Top ROE
    # -----------------------------

    st.subheader("Top ROE")

    top_roe = (
        latest[
            [
                "company_name",
                "return_on_equity_pct"
            ]
        ]
        .sort_values(
            "return_on_equity_pct",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_roe,
        use_container_width=True
    )

    st.bar_chart(
        top_roe.set_index("company_name")
    )

    # -----------------------------
    # Net Margin
    # -----------------------------

    st.subheader("Net Profit Margin")

    top_margin = (
        latest[
            [
                "company_name",
                "net_profit_margin_pct"
            ]
        ]
        .sort_values(
            "net_profit_margin_pct",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_margin,
        use_container_width=True
    )

    st.bar_chart(
        top_margin.set_index("company_name")
    )

    # -----------------------------
    # Lowest Debt
    # -----------------------------

    st.subheader("Lowest Debt")

    debt = (
        latest[
            [
                "company_name",
                "debt_to_equity"
            ]
        ]
        .sort_values(
            "debt_to_equity"
        )
        .head(10)
    )

    st.dataframe(
        debt,
        use_container_width=True
    )

    st.bar_chart(
        debt.set_index("company_name")
    )