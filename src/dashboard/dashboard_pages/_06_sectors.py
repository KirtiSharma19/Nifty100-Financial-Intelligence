import plotly.express as px
import streamlit as st

from src.services.ratio_engine import DatasetBuilder


def show():

    st.title("Sector Analysis")

    engine = DatasetBuilder()

    df = engine.build_dataset()

    latest_year = df["year"].max()

    data = df[df["year"] == latest_year].copy()

    sectors = sorted(data["broad_sector"].dropna().unique())

    sector = st.selectbox("Select Sector", sectors)

    sector_df = data[data["broad_sector"] == sector]

    st.subheader(f"{sector} Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Companies", sector_df["company_name"].nunique())

    col2.metric("Average ROE", round(sector_df["return_on_equity_pct"].mean(), 2))

    col3.metric("Average Quality", round(sector_df["quality_score"].mean(), 2))

    st.divider()

    st.subheader("Sector Bubble Chart")

    fig = px.scatter(
        sector_df,
        x="return_on_equity_pct",
        y="net_profit_margin_pct",
        size="market_cap_crore",
        color="sub_sector",
        hover_name="company_name",
        title=f"{sector} Companies",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Top Companies")

    top = sector_df.sort_values("composite_score", ascending=False).head(10)

    st.dataframe(
        top[
            [
                "company_name",
                "sub_sector",
                "quality_score",
                "composite_score",
                "return_on_equity_pct",
                "net_profit_margin_pct",
                "market_cap_crore",
            ]
        ],
        use_container_width=True,
    )

    st.divider()

    st.subheader("Average Metrics")

    summary = {
        "Average ROE": round(sector_df["return_on_equity_pct"].mean(), 2),
        "Average Margin": round(sector_df["net_profit_margin_pct"].mean(), 2),
        "Average Debt": round(sector_df["debt_to_equity"].mean(), 2),
        "Average PE": round(sector_df["pe_ratio"].mean(), 2),
        "Average PB": round(sector_df["pb_ratio"].mean(), 2),
        "Average Composite": round(sector_df["composite_score"].mean(), 2),
    }

    st.table(summary)

    st.divider()

    st.subheader("Composite Score Distribution")

    fig = px.bar(top, x="company_name", y="composite_score", color="sub_sector")

    st.plotly_chart(fig, use_container_width=True)
