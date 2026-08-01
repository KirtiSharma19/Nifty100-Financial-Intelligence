import streamlit as st
import plotly.express as px

from src.services.ratio_engine import DatasetBuilder


def show():

    st.title("Company Profile")

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

    company_df = df[
        df["company_name"] == company
    ].sort_values("year")

    latest = company_df.iloc[-1]

    st.subheader(company)

    c1, c2 = st.columns(2)

    c1.write(f"**Sector :** {latest['broad_sector']}")
    c2.write(f"**Sub Sector :** {latest['sub_sector']}")

    st.divider()

    st.subheader("Key Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Quality Score",
        latest["quality_score"]
    )

    col2.metric(
        "Composite Score",
        latest["composite_score"]
    )

    col3.metric(
        "ROE %",
        round(
            latest["return_on_equity_pct"],
            2
        )
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Net Margin %",
        round(
            latest["net_profit_margin_pct"],
            2
        )
    )

    col5.metric(
        "Debt / Equity",
        round(
            latest["debt_to_equity"],
            2
        )
    )

    col6.metric(
        "PE Ratio",
        round(
            latest["pe_ratio"],
            2
        )
    )

    st.divider()

    st.subheader("Market Information")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Market Cap",
        f"{latest['market_cap_crore']:,.0f} Cr"
    )

    col2.metric(
        "Enterprise Value",
        f"{latest['enterprise_value_crore']:,.0f}"
    )

    col3.metric(
        "PB Ratio",
        round(
            latest["pb_ratio"],
            2
        )
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "EV / EBITDA",
        round(
            latest["ev_ebitda"],
            2
        )
    )

    col5.metric(
        "Dividend Yield %",
        round(
            latest["dividend_yield_pct"],
            2
        )
    )

    col6.metric(
        "Free Cash Flow",
        round(
            latest["free_cash_flow_cr"],
            2
        )
    )

    st.divider()

    st.subheader("Sales Trend")

    fig = px.line(
        company_df,
        x="year",
        y="sales",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Net Profit Trend")

    fig = px.line(
        company_df,
        x="year",
        y="net_profit",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Operating Profit Trend")

    fig = px.bar(
        company_df,
        x="year",
        y="operating_profit"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("ROE Trend")

    fig = px.line(
        company_df,
        x="year",
        y="return_on_equity_pct",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Historical Financial Data")

    st.dataframe(
        company_df[
            [
                "year",
                "sales",
                "net_profit",
                "operating_profit",
                "return_on_equity_pct",
                "net_profit_margin_pct",
                "debt_to_equity",
                "pe_ratio",
                "pb_ratio",
                "quality_score",
                "composite_score"
            ]
        ],
        use_container_width=True
    )