import pytest
import pandas as pd

from src.etl.normalizer import DataNormalizer


@pytest.mark.parametrize(
    "value, expected",
    [
        # Basic integer years
        (2024, 2024),
        (2023, 2023),
        (2000, 2000),
        (1999, 1999),

        # String years
        ("2024", 2024),
        ("2023", 2023),
        (" 2024 ", 2024),
        (" 2023 ", 2023),

        # FY formats
        ("FY24", 2024),
        ("FY23", 2023),
        ("FY25", 2025),
        ("FY20", 2020),

        # Lower/mixed case FY
        ("fy24", 2024),
        ("Fy23", 2023),

        # Other text containing year
        ("FY2024", 2024),
        ("Year 2024", 2024),

        # Missing values
        (None, None),
        (float("nan"), None),

        # No digits
        ("Unknown", None),
        # Empty string
        ("", None),
    ],
)
def test_normalize_year(value, expected):
    """Test normalize_year across supported formats and edge cases."""
    result = DataNormalizer.normalize_year(value)

    if expected is None:
        assert result is None
    else:
        assert result == expected