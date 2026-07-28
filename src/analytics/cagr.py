class CAGRCalculator:

    @staticmethod
    def calculate(start_value, end_value, years):

        if years <= 0:
            return None

        if start_value == 0:
            return None

        if start_value < 0 and end_value > 0:
            return None

        if start_value > 0 and end_value < 0:
            return None

        if start_value < 0 and end_value < 0:
            return None

        cagr = ((end_value / start_value) ** (1 / years) - 1) * 100

        return round(cagr, 2)