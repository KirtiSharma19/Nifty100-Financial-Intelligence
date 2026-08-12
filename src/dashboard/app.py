import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

from src.dashboard.dashboard_pages._01_home import show as home_page
from src.dashboard.dashboard_pages._02_profile import show as profile_page
from src.dashboard.dashboard_pages._03_screener import show as screener_page
from src.dashboard.dashboard_pages._04_peers import show as peers_page
from src.dashboard.dashboard_pages._05_trends import show as trends_page
from src.dashboard.dashboard_pages._06_sectors import show as sectors_page
from src.dashboard.dashboard_pages._07_capital import show as capital_page
from src.dashboard.dashboard_pages._08_reports import show as reports_page

# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.set_page_config(
    page_title="Nifty100 Financial Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Screen",
    [
        "Home",
        "Company Profile",
        "Financial Screener",
        "Peer Comparison",
        "Trend Analysis",
        "Sector Analysis",
        "Capital Allocation",
        "Reports",
    ],
)

# -------------------------------------------------
# Routing
# -------------------------------------------------

if page == "Home":

    home_page()

elif page == "Company Profile":

    profile_page()

elif page == "Financial Screener":

    screener_page()

elif page == "Peer Comparison":

    peers_page()

elif page == "Trend Analysis":

    trends_page()

elif page == "Sector Analysis":

    sectors_page()

elif page == "Capital Allocation":

    capital_page()

elif page == "Reports":

    reports_page()
