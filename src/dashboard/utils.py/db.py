import streamlit as st

from src.services.ratio_engine import DatasetBuilder


@st.cache_data(ttl=600)
def load_dataset():

    engine = DatasetBuilder()

    return engine.build_dataset()


@st.cache_data(ttl=600)
def get_latest_data():

    df = load_dataset()

    latest_year = df["year"].max()

    return df[df["year"] == latest_year]


@st.cache_data(ttl=600)
def get_companies():

    df = get_latest_data()

    return sorted(df["company_name"].dropna().unique())


@st.cache_data(ttl=600)
def get_company(company_name):

    df = load_dataset()

    return df[df["company_name"] == company_name]


@st.cache_data(ttl=600)
def get_sectors():

    df = get_latest_data()

    return sorted(df["broad_sector"].dropna().unique())


@st.cache_data(ttl=600)
def get_sector(sector):

    df = get_latest_data()

    return df[df["broad_sector"] == sector]
