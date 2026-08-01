import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.services.ratio_engine import DatasetBuilder


def show():

    st.title("Peer Comparison")

    engine = DatasetBuilder()

    df = engine.build_dataset()

    latest_year = df["year"].max()

    data = df[df["year"] == latest_year].copy()

    groups = sorted(
        data["broad_sector"].dropna().unique()
    )

    sector = st.selectbox(
        "Select Peer Group",
        groups
    )

    peer = data[
        data["broad_sector"] == sector
    ]

    companies = sorted(
        peer["company_name"].unique()
    )

    company = st.selectbox(
        "Select Company",
        companies
    )

    selected = peer[
        peer["company_name"] == company
    ].iloc[0]

    metrics = [

        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "quality_score",
        "composite_score",
        "pe_ratio",
        "pb_ratio",
        "dividend_yield_pct"

    ]

    company_values = [
        selected[m]
        for m in metrics
    ]

    peer_values = [

        peer[m].mean()

        for m in metrics

    ]

    fig = go.Figure()

    fig.add_trace(

        go.Scatterpolar(

            r=company_values,

            theta=metrics,

            fill="toself",

            name=company

        )

    )

    fig.add_trace(

        go.Scatterpolar(

            r=peer_values,

            theta=metrics,

            fill="toself",

            name="Peer Average"

        )

    )

    fig.update_layout(

        polar=dict(

            radialaxis=dict(
                visible=True
            )

        ),

        showlegend=True

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    st.subheader("Peer Comparison Table")

    table = peer[

        [

            "company_name",
            "quality_score",
            "composite_score",
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "pe_ratio",
            "pb_ratio"

        ]

    ].sort_values(

        "composite_score",

        ascending=False

    )

    st.dataframe(

        table,

        use_container_width=True

    )

    st.divider()

    st.subheader("Top Companies")

    st.bar_chart(

        table.set_index(
            "company_name"
        )["composite_score"]

    )