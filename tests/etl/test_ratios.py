import pandas as pd

from src.analytics.ratios import (
    RatioEngine,
    calculate_ratios,
)

# ============================================================
# SAFE DIVIDE TESTS
# ============================================================


def test_safe_divide_normal():
    result = RatioEngine.safe_divide(100, 20)

    assert result == 5


def test_safe_divide_zero_denominator():
    result = RatioEngine.safe_divide(100, 0)

    assert result is None


def test_safe_divide_none_denominator():
    result = RatioEngine.safe_divide(100, None)

    assert result is None


def test_safe_divide_nan_denominator():
    result = RatioEngine.safe_divide(100, float("nan"))

    assert result is None


# ============================================================
# NET PROFIT MARGIN TESTS
# ============================================================


def test_net_profit_margin_normal():
    result = RatioEngine.net_profit_margin(20, 100)

    assert result == 20.0


def test_net_profit_margin_negative_profit():
    result = RatioEngine.net_profit_margin(-10, 100)

    assert result == -10.0


def test_net_profit_margin_zero_sales():
    result = RatioEngine.net_profit_margin(20, 0)

    assert result is None


def test_net_profit_margin_none_sales():
    result = RatioEngine.net_profit_margin(20, None)

    assert result is None


# ============================================================
# OPERATING PROFIT MARGIN TESTS
# ============================================================


def test_operating_profit_margin_normal():
    result = RatioEngine.operating_profit_margin(25, 100)

    assert result == 25.0


def test_operating_profit_margin_negative_profit():
    result = RatioEngine.operating_profit_margin(-15, 100)

    assert result == -15.0


def test_operating_profit_margin_zero_sales():
    result = RatioEngine.operating_profit_margin(25, 0)

    assert result is None


def test_operating_profit_margin_none_sales():
    result = RatioEngine.operating_profit_margin(25, None)

    assert result is None


# ============================================================
# DEBT TO EQUITY TESTS
# ============================================================


def test_debt_to_equity_normal():
    result = RatioEngine.debt_to_equity(50, 100)

    assert result == 0.5


def test_debt_to_equity_debt_free():
    result = RatioEngine.debt_to_equity(0, 100)

    assert result == 0


def test_debt_to_equity_zero_equity():
    result = RatioEngine.debt_to_equity(50, 0)

    assert result is None


def test_debt_to_equity_negative_equity():
    result = RatioEngine.debt_to_equity(50, -100)

    assert result == -0.5


# ============================================================
# RETURN ON EQUITY TESTS
# ============================================================


def test_return_on_equity_normal():
    result = RatioEngine.return_on_equity(20, 100)

    assert result == 20.0


def test_return_on_equity_negative_profit():
    result = RatioEngine.return_on_equity(-20, 100)

    assert result == -20.0


def test_return_on_equity_zero_equity():
    result = RatioEngine.return_on_equity(20, 0)

    assert result is None


def test_return_on_equity_none_equity():
    result = RatioEngine.return_on_equity(20, None)

    assert result is None


# ============================================================
# CALCULATE RATIOS - BASIC TEST
# ============================================================


def test_calculate_ratios_basic():

    pl_df = pd.DataFrame(
        {
            "company_id": ["TEST"],
            "year": [2024],
            "net_profit": [10],
            "sales": [100],
            "operating_profit": [20],
            "other_income": [5],
            "interest": [5],
        }
    )

    bs_df = pd.DataFrame(
        {
            "company_id": ["TEST"],
            "year": [2024],
            "equity_capital": [50],
            "reserves": [10],
            "borrowings": [40],
            "total_assets": [200],
        }
    )

    result = calculate_ratios(pl_df, bs_df)

    assert len(result) == 1

    assert "net_profit_margin_pct" in result.columns
    assert "operating_profit_margin_pct" in result.columns
    assert "return_on_equity_pct" in result.columns
    assert "debt_to_equity" in result.columns
    assert "roce_pct" in result.columns
    assert "roa_pct" in result.columns
    assert "interest_coverage" in result.columns
    assert "asset_turnover" in result.columns


# ============================================================
# CALCULATE RATIOS - VALUE TEST
# ============================================================


def test_calculate_ratios_values():

    pl_df = pd.DataFrame(
        {
            "company_id": ["TEST"],
            "year": [2024],
            "net_profit": [10],
            "sales": [100],
            "operating_profit": [20],
            "other_income": [5],
            "interest": [5],
        }
    )

    bs_df = pd.DataFrame(
        {
            "company_id": ["TEST"],
            "year": [2024],
            "equity_capital": [50],
            "reserves": [10],
            "borrowings": [40],
            "total_assets": [200],
        }
    )

    result = calculate_ratios(pl_df, bs_df)

    row = result.iloc[0]

    # Net Profit Margin
    assert row["net_profit_margin_pct"] == 10.0

    # Operating Profit Margin
    assert row["operating_profit_margin_pct"] == 20.0

    # Return on Equity
    # 10 / (50 + 10) * 100 = 16.67%
    assert round(row["return_on_equity_pct"], 2) == 16.67

    # Debt to Equity
    # 40 / (50 + 10) = 0.6667
    assert round(row["debt_to_equity"], 4) == round(40 / 60, 4)

    # ROCE
    # 20 / (50 + 10 + 40) * 100 = 20%
    assert row["roce_pct"] == 20.0

    # ROA
    # 10 / 200 * 100 = 5%
    assert row["roa_pct"] == 5.0

    # Interest Coverage
    # (20 + 5) / 5 = 5
    assert row["interest_coverage"] == 5.0

    # Asset Turnover
    # 100 / 200 = 0.5
    assert row["asset_turnover"] == 0.5


# ============================================================
# CALCULATE RATIOS - ZERO SALES TEST
# ============================================================


def test_calculate_ratios_zero_sales():

    pl_df = pd.DataFrame(
        {
            "company_id": ["TEST"],
            "year": [2024],
            "net_profit": [10],
            "sales": [0],
            "operating_profit": [20],
            "other_income": [5],
            "interest": [5],
        }
    )

    bs_df = pd.DataFrame(
        {
            "company_id": ["TEST"],
            "year": [2024],
            "equity_capital": [50],
            "reserves": [10],
            "borrowings": [40],
            "total_assets": [200],
        }
    )

    result = calculate_ratios(pl_df, bs_df)

    row = result.iloc[0]

    assert pd.isna(row["net_profit_margin_pct"])
    assert pd.isna(row["operating_profit_margin_pct"])


# ============================================================
# CALCULATE RATIOS - ZERO INTEREST TEST
# ============================================================


def test_calculate_ratios_zero_interest():

    pl_df = pd.DataFrame(
        {
            "company_id": ["TEST"],
            "year": [2024],
            "net_profit": [10],
            "sales": [100],
            "operating_profit": [20],
            "other_income": [5],
            "interest": [0],
        }
    )

    bs_df = pd.DataFrame(
        {
            "company_id": ["TEST"],
            "year": [2024],
            "equity_capital": [50],
            "reserves": [10],
            "borrowings": [0],
            "total_assets": [200],
        }
    )

    result = calculate_ratios(pl_df, bs_df)

    row = result.iloc[0]

    assert pd.isna(row["interest_coverage"])
    assert row["icr_label"] == "Debt Free"
