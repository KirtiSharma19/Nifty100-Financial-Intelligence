
from fastapi import APIRouter, Query

from src.services.ratio_engine import DatasetBuilder

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"],
)


def clean_value(value):
    """Convert pandas/numpy values to JSON-safe values."""

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


def get_latest_data():
    """Load latest-year data with one row per company."""

    df = DatasetBuilder().build_dataset()

    df["year"] = df["year"].astype(str).str.extract(r"(\d{4})")[0]

    df["year"] = df["year"].astype(int)

    latest_year = df["year"].max()

    latest = df[df["year"] == latest_year].copy()

    latest = latest.drop_duplicates(subset=["company_id"], keep="first").reset_index(
        drop=True
    )

    return latest


@router.get("")
def get_portfolio(
    companies: str | None = Query(
        default=None, description="Comma-separated company IDs"
    ),
    sector: str | None = Query(
        default=None, description="Filter portfolio by sector"
    ),
):
    """
    Return portfolio-level financial statistics.
    """

    df = get_latest_data()

    # --------------------------------------------------
    # COMPANY FILTER
    # --------------------------------------------------

    if companies:

        company_list = [
            company.strip().upper()
            for company in companies.split(",")
            if company.strip()
        ]

        df = df[df["company_id"].astype(str).str.upper().isin(company_list)]

    # --------------------------------------------------
    # SECTOR FILTER
    # --------------------------------------------------

    if sector:

        df = df[
            df["broad_sector"].astype(str).str.contains(sector, case=False, na=False)
        ]

    # --------------------------------------------------
    # EMPTY PORTFOLIO
    # --------------------------------------------------

    if df.empty:
        return {
            "company_count": 0,
            "companies": [],
            "sector_distribution": {},
            "statistics": {},
        }

    # --------------------------------------------------
    # SECTOR DISTRIBUTION
    # --------------------------------------------------

    sector_counts = df["broad_sector"].fillna("Unknown").value_counts().to_dict()

    total_companies = len(df)

    sector_distribution = {}

    for name, count in sector_counts.items():

        sector_distribution[name] = {
            "count": int(count),
            "percentage": round((count / total_companies) * 100, 2),
        }

    # --------------------------------------------------
    # PORTFOLIO STATISTICS
    # --------------------------------------------------

    statistics = {}

    numeric_metrics = {
        "roe_pct": "return_on_equity_pct",
        "debt_to_equity": "debt_to_equity",
        "revenue_cagr_5yr": "revenue_cagr_5yr",
        "fcf_cagr_5yr": "fcf_cagr_5yr",
        "operating_margin_pct": "operating_profit_margin_pct",
        "net_profit_margin_pct": "net_profit_margin_pct",
        "quality_score": "quality_score",
        "composite_score": "composite_score",
    }

    for output_name, column in numeric_metrics.items():

        if column not in df.columns:
            continue

        values = df[column].dropna()

        if values.empty:
            continue

        statistics[output_name] = {
            "mean": round(float(values.mean()), 2),
            "median": round(float(values.median()), 2),
            "minimum": round(float(values.min()), 2),
            "maximum": round(float(values.max()), 2),
            "std": round(float(values.std()), 2),
        }

    # --------------------------------------------------
    # COMPANY LIST
    # --------------------------------------------------

    company_results = []

    for _, row in df.iterrows():

        company_results.append(
            {
                "company_id": row["company_id"],
                "company_name": row["company_name"],
                "broad_sector": row["broad_sector"],
                "roe_pct": clean_value(row.get("return_on_equity_pct")),
                "debt_to_equity": clean_value(row.get("debt_to_equity")),
                "quality_score": clean_value(row.get("quality_score")),
                "composite_score": clean_value(row.get("composite_score")),
            }
        )

    return {
        "year": int(df["year"].max()),
        "company_count": len(df),
        "companies": company_results,
        "sector_distribution": sector_distribution,
        "statistics": statistics,
    }
