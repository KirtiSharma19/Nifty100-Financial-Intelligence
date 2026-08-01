import streamlit as st
import plotly.express as px

from src.services.ratio_engine import DatasetBuilder


def show():

    st.title("Trend Analysis")

    engine = DatasetBuilder()

    df = engine.build_dataset()

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

    company_df = (
        df[df["company_name"] == company]
        .sort_values("year")
    )

    metrics = [

        "sales",
        "net_profit",
        "operating_profit",
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr"

    ]

    selected_metrics = st.multiselect(

        "Select Metrics",

        metrics,

        default=[
            "sales",
            "net_profit"
        ]

    )

    if len(selected_metrics) == 0:

        st.warning(
            "Select at least one metric."
        )

        return

    st.subheader(company)

    fig = px.line(

        company_df,

        x="year",

        y=selected_metrics,

        markers=True

    )

    fig.update_layout(

        xaxis_title="Year",

        yaxis_title="Value",

        hovermode="x unified"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    st.subheader("Trend Table")

    cols = [

        "year"

    ] + selected_metrics

    st.dataframe(

        company_df[cols],

        use_container_width=True

    )

    st.divider()

    st.subheader("Summary")

    latest = company_df.iloc[-1]

    c1, c2, c3 = st.columns(3)

    c1.metric(

        "Sales",

        f"{latest['sales']:,.0f}"

    )

    c2.metric(

        "Net Profit",

        f"{latest['net_profit']:,.0f}"

    )

    c3.metric(

        "ROE",

        round(
            latest["return_on_equity_pct"],
            2
        )

    )

    c4, c5, c6 = st.columns(3)

    c4.metric(

        "Operating Profit",

        f"{latest['operating_profit']:,.0f}"

    )

    c5.metric(

        "Net Margin",

        round(
            latest["net_profit_margin_pct"],
            2
        )

    )

    c6.metric(

        "Free Cash Flow",

        round(
            latest["free_cash_flow_cr"],
            2
        )

    )

    st.divider()

    st.subheader("Year-wise Financial Data")

    st.dataframe(

        company_df[

            [

                "year",
                "sales",
                "operating_profit",
                "net_profit",
                "return_on_equity_pct",
                "net_profit_margin_pct",
                "operating_profit_margin_pct",
                "debt_to_equity",
                "free_cash_flow_cr"

            ]

        ],

        use_container_width=True

    )