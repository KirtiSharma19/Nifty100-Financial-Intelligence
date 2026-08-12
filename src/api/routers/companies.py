import pandas as pd

from fastapi import APIRouter, HTTPException, Query

from src.utils.database import get_table
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from src.services.ratio_engine import DatasetBuilder


router = APIRouter(
    prefix="/companies",
    tags=["Companies"],
)


def get_latest_companies():
    """
    Build the financial dataset and return one latest-year
    record for every company.
    """

    df = DatasetBuilder().build_dataset()

    # Make sure year is numeric
    df["year"] = df["year"].astype(int)

    # Latest year available in the dataset
    latest_year = df["year"].max()

    latest = df[df["year"] == latest_year].copy()

    # Safety: one record per company
    latest = (
        latest
        .sort_values(["company_id", "year"])
        .drop_duplicates(
            subset=["company_id"],
            keep="first"
        )
    )

    return latest


def get_market_cap_category(value):
    """
    Categorise companies based on market capitalisation.
    """

    if value is None:
        return None

    if value >= 100000:
        return "Large Cap"

    if value >= 20000:
        return "Mid Cap"

    return "Small Cap"


def clean_value(value):
    """
    Convert pandas/numpy values into JSON-safe values.
    """

    if value is None:
        return None

    try:
        if value != value:
            return None
    except Exception:
        pass

    try:
        return float(value)
    except (TypeError, ValueError):
        return value


@router.get("")
def get_companies(
    sector: Optional[str] = Query(
        default=None,
        description="Filter by broad sector"
    ),
    market_cap_category: Optional[str] = Query(
        default=None,
        description="Large Cap, Mid Cap or Small Cap"
    ),
    search: Optional[str] = Query(
        default=None,
        description="Search by company name or ticker"
    ),
):
    """
    Return all companies with optional filters.
    """

    df = get_latest_companies()

    # -----------------------------
    # Sector filter
    # -----------------------------

    if sector:
        df = df[
            df["broad_sector"]
            .astype(str)
            .str.contains(
                sector,
                case=False,
                na=False
            )
        ]

    # -----------------------------
    # Search filter
    # -----------------------------

    if search:
        name_match = (
            df["company_name"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        )

        ticker_match = (
            df["company_id"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        )

        df = df[name_match | ticker_match]

    # -----------------------------
    # Market-cap category
    # -----------------------------

    df["market_cap_category"] = (
        df["market_cap_crore"]
        .apply(get_market_cap_category)
    )

    if market_cap_category:
        df = df[
            df["market_cap_category"]
            .astype(str)
            .str.lower()
            == market_cap_category.lower()
        ]

    # -----------------------------
    # Build response
    # -----------------------------

    result = []

    for _, row in df.iterrows():

        result.append(
            {
                "id": row["company_id"],
                "company_name": row["company_name"],
                "broad_sector": row["broad_sector"],
                "sub_sector": row["sub_sector"],
                "roe_pct": clean_value(
                    row.get("return_on_equity_pct")
                ),
                "roce_pct": clean_value(
                    row.get("roce_pct")
                ),
                "market_cap_category": row[
                    "market_cap_category"
                ],
            }
        )

    return {
        "count": len(result),
        "companies": result,
    }

@router.get("/{ticker}")
def get_company_profile(ticker: str):
    """
    Return full company profile with latest-year KPIs and sector data.
    """

    df = get_latest_companies()

    # Ticker/company ID search
    company = df[
        df["company_id"]
        .astype(str)
        .str.upper()
        == ticker.upper()
    ]

    # Company not found
    if company.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Company '{ticker}' not found"
        )

    row = company.iloc[0]

    # Return all available company fields
    profile = {}

    for column in df.columns:
        value = row[column]

        profile[column] = clean_value(value)

    return profile

@router.get("/{ticker}/pl")
def get_company_profit_loss(
    ticker: str,
    from_year: str | None = None,
    to_year: str | None = None
):
    """
    Return profit and loss history for a company.
    Supports optional from_year and to_year filters.
    """

    # Load company master
    companies = get_table("companies")

    company = companies[
        companies["id"]
        .astype(str)
        .str.upper()
        == ticker.upper()
    ]

    if company.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Company '{ticker}' not found"
        )

    company_id = company.iloc[0]["id"]

    # Load P&L
    pl = get_table("profitandloss")

    pl = pl[
        pl["company_id"].astype(str).str.upper()
        == str(company_id).upper()
    ].copy()

    if pl.empty:
        return {
            "company_id": company_id,
            "company_name": company.iloc[0]["company_name"],
            "history": []
        }

    # Convert year into numeric year
    pl["year_num"] = (
        pl["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    pl["year_num"] = pd.to_numeric(
        pl["year_num"],
        errors="coerce"
    )

    # Validate from_year
    if from_year is not None:

        try:
            from_year_num = int(from_year[:4])
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=400,
                detail="from_year must be in YYYY-MM format"
            )

        pl = pl[
            pl["year_num"] >= from_year_num
        ]

    # Validate to_year
    if to_year is not None:

        try:
            to_year_num = int(to_year[:4])
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=400,
                detail="to_year must be in YYYY-MM format"
            )

        pl = pl[
            pl["year_num"] <= to_year_num
        ]

    # Remove helper column
    pl = pl.drop(columns=["year_num"])

    # Convert NaN values to None
    records = pl.where(
        pd.notna(pl),
        None
    ).to_dict(orient="records")

    return {
        "company_id": company_id,
        "company_name": company.iloc[0]["company_name"],
        "history": records
    }

@router.get("/{ticker}/cashflow")
def get_company_cashflow(
    ticker: str,
    from_year: str | None = None,
    to_year: str | None = None
):
    """
    Return cash flow history for a company.
    Supports optional YYYY-MM year filters.
    """

    companies = get_table("companies")

    company = companies[
        companies["id"]
        .astype(str)
        .str.upper()
        == ticker.upper()
    ]

    if company.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Company '{ticker}' not found"
        )

    company_id = company.iloc[0]["id"]

    cf = get_table("cashflow")

    cf = cf[
        cf["company_id"]
        .astype(str)
        .str.upper()
        == str(company_id).upper()
    ].copy()

    if cf.empty:
        return {
            "company_id": company_id,
            "company_name": company.iloc[0]["company_name"],
            "history": []
        }

    # --------------------------------------------------
    # Clean year
    # --------------------------------------------------

    cf["year_num"] = (
        cf["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    cf["year_num"] = pd.to_numeric(
        cf["year_num"],
        errors="coerce"
    )

    # --------------------------------------------------
    # From year
    # --------------------------------------------------

    if from_year is not None:

        try:
            from_year_num = int(
                from_year[:4]
            )
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=400,
                detail="from_year must be in YYYY-MM format"
            )

        cf = cf[
            cf["year_num"] >= from_year_num
        ]

    # --------------------------------------------------
    # To year
    # --------------------------------------------------

    if to_year is not None:

        try:
            to_year_num = int(
                to_year[:4]
            )
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=400,
                detail="to_year must be in YYYY-MM format"
            )

        cf = cf[
            cf["year_num"] <= to_year_num
        ]

    cf = cf.drop(
        columns=["year_num"]
    )

    records = (
        cf
        .where(pd.notna(cf), None)
        .to_dict(orient="records")
    )

    return {
        "company_id": company_id,
        "company_name": company.iloc[0]["company_name"],
        "history": records
    }

@router.get("/{ticker}/bs")
def get_company_balance_sheet(
    ticker: str,
    from_year: str | None = None,
    to_year: str | None = None
):
    """
    Return balance sheet history for a company.
    Supports optional YYYY-MM year filters.
    """

    companies = get_table("companies")

    company = companies[
        companies["id"]
        .astype(str)
        .str.upper()
        == ticker.upper()
    ]

    if company.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Company '{ticker}' not found"
        )

    company_id = company.iloc[0]["id"]

    bs = get_table("balancesheet")

    bs = bs[
        bs["company_id"]
        .astype(str)
        .str.upper()
        == str(company_id).upper()
    ].copy()

    if bs.empty:
        return {
            "company_id": company_id,
            "company_name": company.iloc[0]["company_name"],
            "history": []
        }

    # ---------------------------------------------
    # Clean year
    # ---------------------------------------------

    bs["year_num"] = (
        bs["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    bs["year_num"] = pd.to_numeric(
        bs["year_num"],
        errors="coerce"
    )

    # ---------------------------------------------
    # From year
    # ---------------------------------------------

    if from_year is not None:

        try:
            from_year_num = int(
                from_year[:4]
            )
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=400,
                detail="from_year must be in YYYY-MM format"
            )

        bs = bs[
            bs["year_num"] >= from_year_num
        ]

    # ---------------------------------------------
    # To year
    # ---------------------------------------------

    if to_year is not None:

        try:
            to_year_num = int(
                to_year[:4]
            )
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=400,
                detail="to_year must be in YYYY-MM format"
            )

        bs = bs[
            bs["year_num"] <= to_year_num
        ]

    bs = bs.drop(
        columns=["year_num"]
    )

    records = (
        bs
        .where(pd.notna(bs), None)
        .to_dict(orient="records")
    )

    return {
        "company_id": company_id,
        "company_name": company.iloc[0]["company_name"],
        "history": records
    }

@router.get("/{ticker}/ratios")
def get_company_ratios(ticker: str):
    """
    Return latest financial ratios and scores
    for a company.
    """

    df = get_latest_companies()

    company = df[
        df["company_id"]
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

    return {
        "company_id": row["company_id"],
        "company_name": row["company_name"],
        "year": int(row["year"]),

        "ratios": {
            "net_profit_margin_pct": clean_value(
                row.get("net_profit_margin_pct")
            ),

            "operating_profit_margin_pct": clean_value(
                row.get("operating_profit_margin_pct")
            ),

            "debt_to_equity": clean_value(
                row.get("debt_to_equity")
            ),

            "return_on_equity_pct": clean_value(
                row.get("return_on_equity_pct")
            ),

            "revenue_cagr_5yr": clean_value(
                row.get("revenue_cagr_5yr")
            ),

            "fcf_cagr_5yr": clean_value(
                row.get("fcf_cagr_5yr")
            ),
        },

        "scores": {
            "quality_score": clean_value(
                row.get("quality_score")
            ),

            "composite_score": clean_value(
                row.get("composite_score")
            ),
        },
    }
@router.get("/{ticker}/tearsheet")
def get_company_tearsheet(ticker: str):
    """
    Return a consolidated financial tearsheet
    for the latest available year.
    """

    df = get_latest_companies()

    company = df[
        df["company_id"]
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

    return {
        # --------------------------------------------------
        # COMPANY
        # --------------------------------------------------

        "company": {
            "company_id": row["company_id"],
            "company_name": row["company_name"],
            "broad_sector": row.get("broad_sector"),
            "sub_sector": row.get("sub_sector"),
            "year": int(row["year"]),
        },

        # --------------------------------------------------
        # PROFITABILITY
        # --------------------------------------------------

        "profitability": {
            "net_profit_margin_pct": clean_value(
                row.get("net_profit_margin_pct")
            ),
            "operating_profit_margin_pct": clean_value(
                row.get("operating_profit_margin_pct")
            ),
            "return_on_equity_pct": clean_value(
                row.get("return_on_equity_pct")
            ),
        },

        # --------------------------------------------------
        # GROWTH
        # --------------------------------------------------

        "growth": {
            "revenue_cagr_5yr": clean_value(
                row.get("revenue_cagr_5yr")
            ),
            "fcf_cagr_5yr": clean_value(
                row.get("fcf_cagr_5yr")
            ),
        },

        # --------------------------------------------------
        # LEVERAGE
        # --------------------------------------------------

        "leverage": {
            "debt_to_equity": clean_value(
                row.get("debt_to_equity")
            ),
        },

        # --------------------------------------------------
        # CASH FLOW
        # --------------------------------------------------

        "cash_flow": {
            "free_cash_flow_cr": clean_value(
                row.get("free_cash_flow_cr")
            ),
            "cash_from_operations_cr": clean_value(
                row.get("cash_from_operations_cr")
            ),
            "capex_cr": clean_value(
                row.get("capex_cr")
            ),
        },

        # --------------------------------------------------
        # VALUATION
        # --------------------------------------------------

        "valuation": {
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
        },

        # --------------------------------------------------
        # SCORES
        # --------------------------------------------------

        "scores": {
            "quality_score": clean_value(
                row.get("quality_score")
            ),
            "composite_score": clean_value(
                row.get("composite_score")
            ),
        },

        # --------------------------------------------------
        # CLUSTER
        # --------------------------------------------------

        "cluster": {
            "cluster_id": clean_value(
                row.get("cluster_id")
            ),
            "cluster_name": row.get(
                "cluster_name"
            ),
        },
    }