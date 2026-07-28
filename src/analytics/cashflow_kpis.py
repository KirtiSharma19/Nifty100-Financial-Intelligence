class CashflowKPI:

    @staticmethod
    def free_cash_flow(cfo, cfi):
        """
        FCF = Operating Cash Flow + Investing Cash Flow
        """
        return cfo + cfi

    @staticmethod
    def capex_intensity(investing_activity, sales):

        if sales == 0:
            return None

        return abs(investing_activity) / sales * 100

    @staticmethod
    def fcf_conversion(fcf, operating_profit):

        if operating_profit == 0:
            return None

        return fcf / operating_profit * 100

    @staticmethod
    def cfo_quality(cfo, pat):

        if pat == 0:
            return None

        return cfo / pat