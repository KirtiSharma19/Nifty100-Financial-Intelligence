from src.analytics.ratios import (
    RatioEngine,
    calculate_ratios,
    calculate_all_ratios,
)


def test_net_profit_margin():
    assert RatioEngine.net_profit_margin(100, 1000) == 10.0


def test_operating_profit_margin():
    assert RatioEngine.operating_profit_margin(250, 1000) == 25.0


def test_debt_to_equity():
    assert RatioEngine.debt_to_equity(500, 1000) == 0.5


def test_roe():
    assert RatioEngine.return_on_equity(250, 1000) == 25.0


def test_zero_sales():
    assert RatioEngine.net_profit_margin(100, 0) is None


def test_zero_equity():
    assert RatioEngine.return_on_equity(100, 0) is None