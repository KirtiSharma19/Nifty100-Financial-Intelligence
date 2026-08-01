import streamlit as st
import plotly.express as px

from src.services.ratio_engine import DatasetBuilder


def show():

    st.title("Nifty100 Financial Intelligence Dashboard")

    engine = DatasetBuilder()

    df = engine.build_dataset()

    # -------------------------
    # Latest Year
    # -------------------------

    latest_year = df["year"].max()

    latest = df[
        df["year"] == latest_year
    ].copy()

    st.subheader(
        f"Financial Summary ({latest_year})"
    )

    # -------------------------
    # KPI Cards
    # -------------------------

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Companies",
        latest["company_name"].nunique()
    )

    c2.metric(
        "Average Quality Score",
        round(
            latest["quality_score"].mean(),
            2
        )
    )

    c3.metric(
        "Average Composite Score",
        round(
            latest["composite_score"].mean(),
            2
        )
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "Average ROE %",
        round(
            latest["return_on_equity_pct"].mean(),
            2
        )
    )

    c5.metric(
        "Average Net Margin %",
        round(
            latest["net_profit_margin_pct"].mean(),
            2
        )
    )

    c6.metric(
        "Average Debt / Equity",
        round(
            latest["debt_to_equity"].mean(),
            2
        )
    )

    st.divider()

    # -------------------------
    # Sector Distribution
    # -------------------------

    st.subheader("Sector Distribution")

    sector = (

        latest

        .groupby("broad_sector")

        .size()

        .reset_index(name="Companies")

    )

    fig = px.pie(

        sector,

        names="broad_sector",

        values="Companies",

        hole=0.45

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # -------------------------
    # Top Companies
    # -------------------------

    st.subheader("Top 10 Companies")

    top = (

        latest

        .sort_values(

            "composite_score",

            ascending=False

        )

        .head(10)

    )

    st.dataframe(

        top[

            [

                "company_name",

                "broad_sector",

                "quality_score",

                "composite_score",

                "return_on_equity_pct",

                "net_profit_margin_pct",

                "debt_to_equity",

                "market_cap_crore"

            ]

        ],

        use_container_width=True

    )

    st.divider()

    # -------------------------
    # Composite Score Chart
    # -------------------------

    st.subheader("Top Composite Scores")

    fig = px.bar(

        top,

        x="company_name",

        y="composite_score",

        color="broad_sector"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # -------------------------
    # Sector Summary
    # -------------------------

    st.subheader("Sector Summary")

    summary = (

        latest

        .groupby("broad_sector")

        .agg(

            {

                "quality_score": "mean",

                "composite_score": "mean",

                "return_on_equity_pct": "mean",

                "net_profit_margin_pct": "mean",

                "debt_to_equity": "mean"

            }

        )

        .round(2)

    )

    st.dataframe(

        summary,

        use_container_width=True

    )