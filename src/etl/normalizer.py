"""
normalizer.py

Handles all data normalization tasks before validation and database loading.
"""

import re

import pandas as pd


class DataNormalizer:

    @staticmethod
    def normalize_year(value):
        """
        Convert year to integer.

        Examples:
        2024 -> 2024
        "2024" -> 2024
        "FY24" -> 2024
        """

        if pd.isna(value):
            return None

        value = str(value).strip()

        digits = re.findall(r"\d+", value)

        if not digits:
            return None

        year = int(digits[-1])

        if year < 100:
            year += 2000

        return year

    @staticmethod
    def normalize_ticker(value):
        """
        Normalize company ticker.

        Example:
        tcs
        TCS
        TCS.NS

        =>
        TCS
        """

        if pd.isna(value):
            return ""

        value = str(value).upper().strip()

        value = value.replace(".NS", "")
        value = value.replace(".BO", "")

        return value

    @staticmethod
    def clean_string(value):

        if pd.isna(value):
            return ""

        return str(value).strip()

    @staticmethod
    def clean_dataframe(df):

        df = df.copy()

        for col in df.columns:

            if df[col].dtype == object:
                df[col] = df[col].apply(DataNormalizer.clean_string)

        return df
