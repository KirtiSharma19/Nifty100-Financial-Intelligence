import streamlit as st
import plotly.express as px

from src.services.ratio_engine import DatasetBuilder


def show():

    st.title("Capital Allocation Analysis")

    engine = DatasetBuilder()

    df = engine.build_dataset()

    latest_year = df["year"].max()

    data = df[df["year"] == latest_year].copy()

    companies = sorted(

        df["company_name"]
        .dropna()
        .astype(str)
        .unique()
    )

    company = st.selectbox(
        "Select Company",
        companies
    )

    company_df = data[
        data["company_name"] == company
    ]

    latest = company_df.iloc[0]

    st.subheader(company)

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Cash From Operations",
        f"{latest['cash_from_operations_cr']:,.2f}"
    )

    c2.metric(
        "CAPEX",
        f"{latest['capex_cr']:,.2f}"
    )

    c3.metric(
        "Free Cash Flow",
        f"{latest['free_cash_flow_cr']:,.2f}"
    )

    st.divider()

    st.subheader("Capital Allocation")

    chart = {

        "Metric": [

            "Cash From Operations",
            "CAPEX",
            "Free Cash Flow"

        ],

        "Value": [

            latest["cash_from_operations_cr"],
            latest["capex_cr"],
            latest["free_cash_flow_cr"]

        ]

    }

    fig = px.bar(

        chart,

        x="Metric",

        y="Value",

        text="Value"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    st.subheader("Top Companies by Free Cash Flow")

    top = (

        data

        .sort_values(

            "free_cash_flow_cr",

            ascending=False

        )

        .head(10)

    )

    st.dataframe(

        top[

            [

                "company_name",

                "free_cash_flow_cr",

                "cash_from_operations_cr",

                "capex_cr",

                "quality_score",

                "composite_score"

            ]

        ],

        use_container_width=True

    )

    st.divider()

    st.subheader("Free Cash Flow Distribution")

    fig = px.scatter(

        data,

        x="cash_from_operations_cr",

        y="free_cash_flow_cr",

        size="market_cap_crore",

        color="broad_sector",

        hover_name="company_name"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    st.subheader("Capital Allocation Rankings")

    ranking = data[

        [

            "company_name",

            "cash_from_operations_cr",

            "capex_cr",

            "free_cash_flow_cr",

            "quality_score",

            "composite_score"

        ]

    ].sort_values(

        "free_cash_flow_cr",

        ascending=False

    )

    st.dataframe(

        ranking,

        use_container_width=True

    )