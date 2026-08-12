
from fastapi import APIRouter, Query

from src.services.ratio_engine import DatasetBuilder

router = APIRouter(
    prefix="/screener",
    tags=["Screener"],
)


def get_latest_data():
    """
    Build dataset and keep one latest-year
    record per company.
    """

    df = DatasetBuilder().build_dataset()

    df["year"] = df["year"].astype(str).str.extract(r"(\d{4})")[0].astype(int)

    latest_year = df["year"].max()

    latest = df[df["year"] == latest_year].copy()

    latest = latest.drop_duplicates(subset=["company_id"], keep="first").reset_index(
        drop=True
    )

    return latest


def clean_value(value):
    """Convert pandas NaN values to JSON-safe None."""

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
def screen_companies(
    sector: str | None = Query(default=None),
    min_roe: float | None = Query(default=None),
    max_roe: float | None = Query(default=None),
    min_debt_to_equity: float | None = Query(default=None),
    max_debt_to_equity: float | None = Query(default=None),
    min_revenue_cagr: float | None = Query(default=None),
    min_fcf_cagr: float | None = Query(default=None),
    min_operating_margin: float | None = Query(default=None),
    sort_by: str = Query(default="quality_score"),
    descending: bool = Query(default=True),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    """
    Screen NIFTY100 companies using financial KPIs.
    """

    df = get_latest_data()

    # --------------------------------------------------
    # SECTOR
    # --------------------------------------------------

    if sector:
        df = df[
            df["broad_sector"].astype(str).str.contains(sector, case=False, na=False)
        ]

    # --------------------------------------------------
    # ROE
    # --------------------------------------------------

    if min_roe is not None:
        df = df[df["return_on_equity_pct"] >= min_roe]

    if max_roe is not None:
        df = df[df["return_on_equity_pct"] <= max_roe]

    # --------------------------------------------------
    # DEBT TO EQUITY
    # --------------------------------------------------

    if min_debt_to_equity is not None:
        df = df[df["debt_to_equity"] >= min_debt_to_equity]

    if max_debt_to_equity is not None:
        df = df[df["debt_to_equity"] <= max_debt_to_equity]

    # --------------------------------------------------
    # REVENUE CAGR
    # --------------------------------------------------

    if min_revenue_cagr is not None:
        df = df[df["revenue_cagr_5yr"] >= min_revenue_cagr]

    # --------------------------------------------------
    # FCF CAGR
    # --------------------------------------------------

    if min_fcf_cagr is not None:
        df = df[df["fcf_cagr_5yr"] >= min_fcf_cagr]

    # --------------------------------------------------
    # OPERATING MARGIN
    # --------------------------------------------------

    if min_operating_margin is not None:
        df = df[df["operating_profit_margin_pct"] >= min_operating_margin]

    # --------------------------------------------------
    # SORTING
    # --------------------------------------------------

    allowed_sort_columns = {
        "quality_score",
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "fcf_cagr_5yr",
        "operating_profit_margin_pct",
        "net_profit_margin_pct",
        "composite_score",
        "market_cap_crore",
    }

    if sort_by not in allowed_sort_columns:
        sort_by = "quality_score"

    if sort_by in df.columns:

        df = df.sort_values(sort_by, ascending=not descending, na_position="last")

    # --------------------------------------------------
    # TOTAL RESULTS
    # --------------------------------------------------

    total = len(df)

    # --------------------------------------------------
    # PAGINATION
    # --------------------------------------------------

    start = (page - 1) * page_size

    end = start + page_size

    paginated = df.iloc[start:end]

    # --------------------------------------------------
    # RESPONSE
    # --------------------------------------------------

    results = []

    for _, row in paginated.iterrows():

        results.append(
            {
                "company_id": row["company_id"],
                "company_name": row["company_name"],
                "broad_sector": row["broad_sector"],
                "roe_pct": clean_value(row.get("return_on_equity_pct")),
                "debt_to_equity": clean_value(row.get("debt_to_equity")),
                "revenue_cagr_5yr": clean_value(row.get("revenue_cagr_5yr")),
                "fcf_cagr_5yr": clean_value(row.get("fcf_cagr_5yr")),
                "operating_margin_pct": clean_value(
                    row.get("operating_profit_margin_pct")
                ),
                "quality_score": clean_value(row.get("quality_score")),
                "composite_score": clean_value(row.get("composite_score")),
                "market_cap_crore": clean_value(row.get("market_cap_crore")),
            }
        )

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "results": results,
    }
