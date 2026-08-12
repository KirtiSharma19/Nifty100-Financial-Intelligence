import matplotlib.pyplot as plt
import streamlit as st

from src.services.ratio_engine import DatasetBuilder


def show_company_dashboard():

    # -----------------------------------------
    # Load Dataset
    # -----------------------------------------

    engine = DatasetBuilder()

    df = engine.build_dataset()

    # -----------------------------------------
    # Clean Year
    # -----------------------------------------

    df["year"] = df["year"].astype(str).str.extract(r"(\d{4})")[0].astype(int)

    # -----------------------------------------
    # Company Selection
    # -----------------------------------------

    st.title("Company Dashboard")

    company = st.selectbox(
        "Select Company", sorted(df["company_name"].dropna().unique())
    )

    company_df = df[df["company_name"] == company].sort_values("year")

    latest = company_df.iloc[-1]

    # -----------------------------------------
    # KPI Cards
    # -----------------------------------------

    st.subheader("Financial Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Quality Score", round(latest["quality_score"], 2))

    col2.metric("ROE %", round(latest["return_on_equity_pct"], 2))

    col3.metric("Net Margin %", round(latest["net_profit_margin_pct"], 2))

    col4.metric("Debt / Equity", round(latest["debt_to_equity"], 2))

    st.divider()

    col5, col6, col7, col8 = st.columns(4)

    col5.metric("Free Cash Flow", round(latest["free_cash_flow_cr"], 2))

    col6.metric(
        "Market Cap",
        (
            f"{latest['market_cap_crore']:,.0f}"
            if not st.session_state.get("_dummy")
            and latest["market_cap_crore"] == latest["market_cap_crore"]
            else "-"
        ),
    )

    col7.metric(
        "Enterprise Value",
        (
            f"{latest['enterprise_value_crore']:,.0f}"
            if latest["enterprise_value_crore"] == latest["enterprise_value_crore"]
            else "-"
        ),
    )

    col8.metric(
        "Dividend Yield %",
        (
            round(latest["dividend_yield_pct"], 2)
            if latest["dividend_yield_pct"] == latest["dividend_yield_pct"]
            else "-"
        ),
    )

    st.divider()

    col9, col10, col11 = st.columns(3)

    col9.metric(
        "PE Ratio",
        (
            round(latest["pe_ratio"], 2)
            if latest["pe_ratio"] == latest["pe_ratio"]
            else "-"
        ),
    )

    col10.metric(
        "PB Ratio",
        (
            round(latest["pb_ratio"], 2)
            if latest["pb_ratio"] == latest["pb_ratio"]
            else "-"
        ),
    )

    col11.metric(
        "EV / EBITDA",
        (
            round(latest["ev_ebitda"], 2)
            if latest["ev_ebitda"] == latest["ev_ebitda"]
            else "-"
        ),
    )
    # =====================================================
    # COMPANY TRENDS
    # =====================================================

    st.divider()

    st.header("Company Trends")

    chart1, chart2 = st.columns(2)

    # ---------------- ROE ----------------

    with chart1:

        st.subheader("ROE Trend")

        fig, ax = plt.subplots(figsize=(6, 4))

        ax.plot(
            company_df["year"],
            company_df["return_on_equity_pct"],
            marker="o",
            linewidth=2,
        )

        ax.set_xlabel("Year")
        ax.set_ylabel("ROE %")

        plt.xticks(rotation=45)

        st.pyplot(fig)

    # ---------------- Margin ----------------

    with chart2:

        st.subheader("Net Profit Margin")

        fig, ax = plt.subplots(figsize=(6, 4))

        ax.plot(
            company_df["year"],
            company_df["net_profit_margin_pct"],
            marker="o",
            linewidth=2,
        )

        ax.set_xlabel("Year")
        ax.set_ylabel("Margin %")

        plt.xticks(rotation=45)

        st.pyplot(fig)

    # =====================================================
    # SECOND ROW
    # =====================================================

    chart3, chart4 = st.columns(2)

    with chart3:

        st.subheader("Free Cash Flow")

        fig, ax = plt.subplots(figsize=(6, 4))

        ax.bar(company_df["year"], company_df["free_cash_flow_cr"])

        ax.set_ylabel("Cash Flow (Cr)")

        plt.xticks(rotation=45)

        st.pyplot(fig)

    with chart4:

        st.subheader("Debt / Equity")

        fig, ax = plt.subplots(figsize=(6, 4))

        ax.plot(
            company_df["year"], company_df["debt_to_equity"], marker="o", linewidth=2
        )

        ax.set_ylabel("Debt / Equity")

        plt.xticks(rotation=45)

        st.pyplot(fig)

    # =====================================================
    # THIRD ROW
    # =====================================================

    chart5, chart6 = st.columns(2)

    with chart5:

        st.subheader("Market Cap")

        fig, ax = plt.subplots(figsize=(6, 4))

        ax.plot(
            company_df["year"], company_df["market_cap_crore"], marker="o", linewidth=2
        )

        ax.set_ylabel("Market Cap")

        plt.xticks(rotation=45)

        st.pyplot(fig)

    with chart6:

        st.subheader("Enterprise Value")

        fig, ax = plt.subplots(figsize=(6, 4))

        ax.plot(
            company_df["year"],
            company_df["enterprise_value_crore"],
            marker="o",
            linewidth=2,
        )

        ax.set_ylabel("Enterprise Value")

        plt.xticks(rotation=45)

        st.pyplot(fig)

    # =====================================================
    # COMPANY HISTORY
    # =====================================================

    st.divider()

    st.header("Company Financial History")

    history_columns = [
        "year",
        "quality_score",
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "market_cap_crore",
        "enterprise_value_crore",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "dividend_yield_pct",
    ]

    available_columns = [col for col in history_columns if col in company_df.columns]

    st.dataframe(
        company_df[available_columns].sort_values("year", ascending=False),
        use_container_width=True,
    )

    # =====================================================
    # VALUATION SUMMARY
    # =====================================================

    st.divider()

    st.header("Valuation Summary")

    left, right = st.columns(2)

    with left:

        st.info(f"""
**Current PE Ratio**

{latest['pe_ratio']:.2f}

**PB Ratio**

{latest['pb_ratio']:.2f}

**EV / EBITDA**

{latest['ev_ebitda']:.2f}
""")

    with right:

        st.success(f"""
**Market Cap**

₹ {latest['market_cap_crore']:,.0f} Cr

**Enterprise Value**

₹ {latest['enterprise_value_crore']:,.0f} Cr

**Dividend Yield**

{latest['dividend_yield_pct']:.2f} %
""")

    # =====================================================
    # DOWNLOAD REPORT
    # =====================================================

    csv = company_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Company Report (CSV)",
        data=csv,
        file_name=f"{company}_financial_report.csv",
        mime="text/csv",
    )

    # =====================================================
    # FOOTER
    # =====================================================

    st.divider()

    st.caption(
        "Nifty100 Financial Intelligence Dashboard | Built using Python, Pandas & Streamlit"
    )
