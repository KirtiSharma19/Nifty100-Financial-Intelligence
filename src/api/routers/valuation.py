from fastapi import APIRouter, HTTPException

import pandas as pd

from src.services.ratio_engine import DatasetBuilder


router = APIRouter(
    prefix="/valuation",
    tags=["Valuation"],
)


def clean_value(value):
    """Convert pandas/numpy missing values to JSON-safe values."""

    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    try:
        return float(value)
    except (TypeError, ValueError):
        return value


@router.get("/{ticker}")
def get_valuation(ticker: str):
    """
    Return latest available valuation metrics
    for a company.
    """

    df = DatasetBuilder().build_dataset()

    # --------------------------------------------------
    # Clean year
    # --------------------------------------------------

    df["year"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    df["year"] = pd.to_numeric(
        df["year"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["year"]
    )

    df["year"] = df["year"].astype(int)

    # --------------------------------------------------
    # Latest year
    # --------------------------------------------------

    latest_year = df["year"].max()

    latest = df[
        df["year"] == latest_year
    ].copy()

    latest = (
        latest
        .drop_duplicates(
            subset=["company_id"],
            keep="first"
        )
    )

    # --------------------------------------------------
    # Find company
    # --------------------------------------------------

    company = latest[
        latest["company_id"]
        .astype(str)
        .str.upper()
        == ticker.upper()
    ]

    if company.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Company '{ticker}' not found"
        )

    row = company.iloc[0]

    # --------------------------------------------------
    # Response
    # --------------------------------------------------

    return {
        "company_id": row["company_id"],
        "company_name": row["company_name"],
        "year": int(row["year"]),

        "market_cap_crore": clean_value(
            row.get("market_cap_crore")
        ),

        "enterprise_value_crore": clean_value(
            row.get("enterprise_value_crore")
        ),

        "pe_ratio": clean_value(
            row.get("pe_ratio")
        ),

        "pb_ratio": clean_value(
            row.get("pb_ratio")
        ),

        "ev_ebitda": clean_value(
            row.get("ev_ebitda")
        ),

        "dividend_yield_pct": clean_value(
            row.get("dividend_yield_pct")
        ),
    }