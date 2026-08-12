import os
from pathlib import Path

import pandas as pd
import streamlit as st


def show():

    st.title("Reports & Downloads")

    st.write("Download generated reports and preview exported data.")

    report_files = {
        "Final Financial Report": "exports/final_financial_report.csv",
        "Sector Report": "exports/sector_report.csv",
        "Cashflow Report": "exports/cashflow_report.csv",
        "CAGR Report": "exports/cagr_report.csv",
        "Valuation Report": "exports/valuation_report.csv",
        "Screener Report": "exports/screener_output.csv",
        "Peer Comparison CSV": "exports/peer_comparison.csv",
        "Peer Comparison Excel": "exports/peer_comparison.xlsx",
    }

    st.header("Available Reports")

    for name, path in report_files.items():

        if os.path.exists(path):

            size = round(os.path.getsize(path) / 1024, 2)

            col1, col2 = st.columns([4, 1])

            with col1:

                st.success(f"{name} ({size} KB)")

            with col2, open(path, "rb") as file:

                st.download_button(
                    "Download",
                    data=file,
                    file_name=Path(path).name,
                    mime="application/octet-stream",
                    key=path,
                )

        else:

            st.error(f"{name} Not Found")

    st.divider()

    st.header("Preview CSV Reports")

    preview = st.selectbox(
        "Select Report",
        [
            "Final Financial Report",
            "Sector Report",
            "Cashflow Report",
            "CAGR Report",
            "Valuation Report",
            "Screener Report",
            "Peer Comparison CSV",
        ],
    )

    file_path = report_files[preview]

    if os.path.exists(file_path):

        df = pd.read_csv(file_path)

        st.dataframe(df.head(20), use_container_width=True)

        st.write(f"Rows : {len(df)}")

        st.write(f"Columns : {len(df.columns)}")

    st.divider()

    st.header("Generated Charts")

    chart_folder = "exports/charts"

    if os.path.exists(chart_folder):

        charts = [file for file in os.listdir(chart_folder) if file.endswith(".png")]

        if charts:

            chart = st.selectbox("Select Chart", charts)

            st.image(os.path.join(chart_folder, chart), width=900)

        else:

            st.info("No charts found.")

    else:

        st.warning("Charts folder not found.")

    st.divider()

    st.success("Sprint 4 Reports Module Completed")
