from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from src.services.ratio_engine import DatasetBuilder


router = APIRouter(
    prefix="/peers",
    tags=["Peers"],
)


def get_latest_data():
    """
    Build dataset and keep one latest-year
    record per company.
    """

    df = DatasetBuilder().build_dataset()

    df["year"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
        .astype(int)
    )

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
        .reset_index(drop=True)
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


@router.get("/{ticker}")
def get_peers(
    ticker: str,
    limit: int = Query(
        default=10,
        ge=1,
        le=50
    ),
    sort_by: str = Query(
        default="quality_score"
    ),
):
    """
    Return companies from the same broad sector
    as the selected company.
    """

    df = get_latest_data()

    # --------------------------------------------------
    # Find target company
    # --------------------------------------------------

    target = df[
        df["company_id"]
        .astype(str)
        .str.upper()
        == ticker.upper()
    ]

    if target.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Company '{ticker}' not found"
        )

    target_row = target.iloc[0]

    target_sector = target_row["broad_sector"]

    # --------------------------------------------------
    # Same-sector peers
    # --------------------------------------------------

    peers = df[
        df["broad_sector"]
        .astype(str)
        .str.lower()
        == str(target_sector).lower()
    ].copy()

    # Remove target company itself
    peers = peers[
        peers["company_id"]
        .astype(str)
        .str.upper()
        != ticker.upper()
    ]

    # --------------------------------------------------
    # Allowed sorting
    # --------------------------------------------------

    allowed_sort_columns = {
        "quality_score",
        "composite_score",
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "fcf_cagr_5yr",
        "operating_profit_margin_pct",
        "net_profit_margin_pct",
        "market_cap_crore",
    }

    if sort_by not in allowed_sort_columns:
        sort_by = "quality_score"

    peers = peers.sort_values(
        sort_by,
        ascending=False,
        na_position="last"
    ).head(limit)

    # --------------------------------------------------
    # Build response
    # --------------------------------------------------

    peer_results = []

    for _, row in peers.iterrows():

        peer_results.append(
            {
                "company_id": row["company_id"],
                "company_name": row["company_name"],
                "broad_sector": row["broad_sector"],
                "sub_sector": row["sub_sector"],
                "roe_pct": clean_value(
                    row.get("return_on_equity_pct")
                ),
                "debt_to_equity": clean_value(
                    row.get("debt_to_equity")
                ),
                "revenue_cagr_5yr": clean_value(
                    row.get("revenue_cagr_5yr")
                ),
                "fcf_cagr_5yr": clean_value(
                    row.get("fcf_cagr_5yr")
                ),
                "operating_margin_pct": clean_value(
                    row.get(
                        "operating_profit_margin_pct"
                    )
                ),
                "net_profit_margin_pct": clean_value(
                    row.get(
                        "net_profit_margin_pct"
                    )
                ),
                "quality_score": clean_value(
                    row.get("quality_score")
                ),
                "composite_score": clean_value(
                    row.get("composite_score")
                ),
                "market_cap_crore": clean_value(
                    row.get("market_cap_crore")
                ),
            }
        )

    return {
        "company": {
            "company_id": target_row["company_id"],
            "company_name": target_row["company_name"],
            "broad_sector": target_row["broad_sector"],
            "sub_sector": target_row["sub_sector"],
        },
        "year": int(target_row["year"]),
        "peer_count": len(peer_results),
        "peers": peer_results,
    }