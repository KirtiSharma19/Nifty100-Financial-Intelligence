import math

import pandas as pd
from fastapi import APIRouter, HTTPException, Query

from src.services.ratio_engine import DatasetBuilder

router = APIRouter(
    prefix="/sectors",
    tags=["Sectors"],
)


# ============================================================
# JSON SAFE VALUE
# ============================================================


def clean_value(value):
    """
    Convert pandas NaN / infinity values into JSON-safe None.
    Keep strings and other normal values unchanged.
    """

    if value is None:
        return None

    if pd.isna(value):
        return None

    if isinstance(value, float):
        if not math.isfinite(value):
            return None

    return value


# ============================================================
# CALCULATE 5-YEAR CAGR
# ============================================================


def calculate_cagr(start_value, end_value, years):
    """
    Calculate CAGR:

        CAGR = ((End / Start) ^ (1 / Years) - 1) * 100

    Returns None when CAGR cannot be calculated safely.
    """

    if start_value is None or end_value is None:
        return None

    if years <= 0:
        return None

    try:
        start_value = float(start_value)
        end_value = float(end_value)

        if not math.isfinite(start_value):
            return None

        if not math.isfinite(end_value):
            return None

        # CAGR is not mathematically meaningful
        # when the starting value is zero or negative.
        if start_value <= 0:
            return None

        if end_value < 0:
            return None

        return round((((end_value / start_value) ** (1 / years)) - 1) * 100, 2)

    except (TypeError, ValueError, ZeroDivisionError):
        return None


# ============================================================
# ADD 5-YEAR CAGR COLUMNS
# ============================================================


def add_cagr_columns(df):
    """
    Add:

        revenue_cagr_5yr
        fcf_cagr_5yr

    using sales and free_cash_flow_cr.
    """

    df = df.copy()

    df["revenue_cagr_5yr"] = None
    df["fcf_cagr_5yr"] = None

    for company_id in df["company_id"].dropna().unique():

        company_df = df[df["company_id"] == company_id].sort_values("year").copy()

        if company_df.empty:
            continue

        latest_year = company_df["year"].max()
        start_year = latest_year - 5

        latest_rows = company_df[company_df["year"] == latest_year]

        start_rows = company_df[company_df["year"] == start_year]

        # A true 5-year CAGR needs both endpoints.
        if latest_rows.empty or start_rows.empty:
            continue

        latest_row = latest_rows.iloc[0]
        start_row = start_rows.iloc[0]

        revenue_cagr = calculate_cagr(
            start_row.get("sales"), latest_row.get("sales"), 5
        )

        fcf_cagr = calculate_cagr(
            start_row.get("free_cash_flow_cr"), latest_row.get("free_cash_flow_cr"), 5
        )

        latest_index = latest_row.name

        df.loc[latest_index, "revenue_cagr_5yr"] = revenue_cagr

        df.loc[latest_index, "fcf_cagr_5yr"] = fcf_cagr

    return df


# ============================================================
# GET LATEST DATA
# ============================================================


def get_latest_data():
    """
    Build the complete dataset.

    Calculate 5-year CAGR using historical records.

    Then keep one latest-year record for every company.
    """

    df = DatasetBuilder().build_dataset()

    # --------------------------------------------------------
    # Normalize year
    # --------------------------------------------------------

    df["year"] = df["year"].astype(str).str.extract(r"(\d{4})")[0].astype(int)

    # --------------------------------------------------------
    # Calculate CAGR BEFORE filtering latest year
    # --------------------------------------------------------

    df = add_cagr_columns(df)

    # --------------------------------------------------------
    # Latest year
    # --------------------------------------------------------

    latest_year = df["year"].max()

    latest = df[df["year"] == latest_year].copy()

    # --------------------------------------------------------
    # One record per company
    # --------------------------------------------------------

    latest = latest.drop_duplicates(subset=["company_id"], keep="first").reset_index(
        drop=True
    )

    return latest


# ============================================================
# GET ALL SECTORS
# ============================================================


@router.get("")
def get_sectors(
    search: str | None = Query(default=None, description="Search sector name")
):
    """
    Return sector-wise financial summary.
    """

    df = get_latest_data()

    # --------------------------------------------------------
    # Remove missing sectors
    # --------------------------------------------------------

    df = df[df["broad_sector"].notna()].copy()

    # --------------------------------------------------------
    # Optional search
    # --------------------------------------------------------

    if search:
        df = df[
            df["broad_sector"].astype(str).str.contains(search, case=False, na=False)
        ]

    # --------------------------------------------------------
    # Sector aggregation
    # --------------------------------------------------------

    sector_summary = (
        df.groupby("broad_sector")
        .agg(
            company_count=("company_id", "nunique"),
            avg_roe_pct=("return_on_equity_pct", "mean"),
            median_roe_pct=("return_on_equity_pct", "median"),
            avg_debt_to_equity=("debt_to_equity", "mean"),
            avg_revenue_cagr_5yr=("revenue_cagr_5yr", "mean"),
            avg_fcf_cagr_5yr=("fcf_cagr_5yr", "mean"),
            avg_operating_margin_pct=("operating_profit_margin_pct", "mean"),
            avg_quality_score=("quality_score", "mean"),
            avg_composite_score=("composite_score", "mean"),
        )
        .reset_index()
    )

    # --------------------------------------------------------
    # Sort by quality score
    # --------------------------------------------------------

    sector_summary = sector_summary.sort_values(
        "avg_quality_score", ascending=False, na_position="last"
    ).round(2)

    # --------------------------------------------------------
    # Build JSON response
    # --------------------------------------------------------

    results = []

    for _, row in sector_summary.iterrows():

        results.append(
            {
                "sector": row["broad_sector"],
                "company_count": int(row["company_count"]),
                "avg_roe_pct": clean_value(row["avg_roe_pct"]),
                "median_roe_pct": clean_value(row["median_roe_pct"]),
                "avg_debt_to_equity": clean_value(row["avg_debt_to_equity"]),
                "avg_revenue_cagr_5yr": clean_value(row["avg_revenue_cagr_5yr"]),
                "avg_fcf_cagr_5yr": clean_value(row["avg_fcf_cagr_5yr"]),
                "avg_operating_margin_pct": clean_value(
                    row["avg_operating_margin_pct"]
                ),
                "avg_quality_score": clean_value(row["avg_quality_score"]),
                "avg_composite_score": clean_value(row["avg_composite_score"]),
            }
        )

    return {
        "count": len(results),
        "year": int(df["year"].max()),
        "sectors": results,
    }


# ============================================================
# GET COMPANIES INSIDE ONE SECTOR
# ============================================================


@router.get("/{sector_name}")
def get_sector_details(sector_name: str, sort_by: str = Query(default="quality_score")):
    """
    Return companies belonging to a specific sector.
    """

    df = get_latest_data()

    # --------------------------------------------------------
    # Filter sector
    # --------------------------------------------------------

    sector_df = df[
        df["broad_sector"].astype(str).str.lower() == sector_name.lower()
    ].copy()

    # --------------------------------------------------------
    # Sector not found
    # --------------------------------------------------------

    if sector_df.empty:
        raise HTTPException(status_code=404, detail=f"Sector '{sector_name}' not found")

    # --------------------------------------------------------
    # Allowed sorting columns
    # --------------------------------------------------------

    allowed_sort_columns = {
        "quality_score",
        "composite_score",
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "fcf_cagr_5yr",
        "operating_profit_margin_pct",
    }

    if sort_by not in allowed_sort_columns:
        sort_by = "quality_score"

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    sector_df = sector_df.sort_values(sort_by, ascending=False, na_position="last")

    # --------------------------------------------------------
    # Build company response
    # --------------------------------------------------------

    companies = []

    for _, row in sector_df.iterrows():

        companies.append(
            {
                "company_id": clean_value(row["company_id"]),
                "company_name": clean_value(row["company_name"]),
                "sub_sector": clean_value(row["sub_sector"]),
                "roe_pct": clean_value(row.get("return_on_equity_pct")),
                "debt_to_equity": clean_value(row.get("debt_to_equity")),
                "revenue_cagr_5yr": clean_value(row.get("revenue_cagr_5yr")),
                "fcf_cagr_5yr": clean_value(row.get("fcf_cagr_5yr")),
                "operating_margin_pct": clean_value(
                    row.get("operating_profit_margin_pct")
                ),
                "quality_score": clean_value(row.get("quality_score")),
                "composite_score": clean_value(row.get("composite_score")),
            }
        )

    # --------------------------------------------------------
    # Final response
    # --------------------------------------------------------

    return {
        "sector": sector_name,
        "year": int(sector_df["year"].max()),
        "company_count": len(companies),
        "companies": companies,
    }
