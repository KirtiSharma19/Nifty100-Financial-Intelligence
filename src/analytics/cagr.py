"""
CAGR Calculator

Provides reusable CAGR calculation logic for
financial analysis.
"""


class CAGRCalculator:
    """
    Calculate Compound Annual Growth Rate (CAGR).
    """

    @staticmethod
    def calculate(start_value, end_value, years):
        """
        Calculate CAGR.

        Formula:
            CAGR = ((End Value / Start Value) ** (1 / Years) - 1) * 100

        Parameters
        ----------
        start_value : float
            Starting value.

        end_value : float
            Ending value.

        years : int or float
            Number of years.

        Returns
        -------
        float or None
            CAGR percentage rounded to 2 decimals.
        """

        # Invalid values
        if start_value is None or end_value is None:
            return None

        if years is None:
            return None

        # Years must be positive
        if years <= 0:
            return None

        # Starting value must be positive
        # because CAGR calculation cannot use zero
        # or negative starting values.
        if start_value <= 0:
            return None

        try:
            cagr = ((end_value / start_value) ** (1 / years) - 1) * 100

            return round(cagr, 2)

        except (TypeError, ValueError, ZeroDivisionError):
            return None
