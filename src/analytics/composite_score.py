class CompositeScore:

    @staticmethod
    def calculate(roe, net_margin, free_cash_flow, debt_to_equity, dividend_yield):

        score = 0

        # -----------------------------
        # ROE (25 Marks)
        # -----------------------------
        if roe is not None:
            if roe >= 20:
                score += 25
            elif roe >= 15:
                score += 20
            elif roe >= 10:
                score += 15
            else:
                score += 5

        # -----------------------------
        # Net Profit Margin (20 Marks)
        # -----------------------------
        if net_margin is not None:
            if net_margin >= 20:
                score += 20
            elif net_margin >= 10:
                score += 15
            elif net_margin >= 5:
                score += 10

        # -----------------------------
        # Free Cash Flow (20 Marks)
        # -----------------------------
        if free_cash_flow is not None:
            if free_cash_flow > 0:
                score += 20

        # -----------------------------
        # Debt To Equity (20 Marks)
        # -----------------------------
        if debt_to_equity is not None:

            if debt_to_equity <= 0.5:
                score += 20

            elif debt_to_equity <= 1:
                score += 15

            elif debt_to_equity <= 2:
                score += 10

        # -----------------------------
        # Dividend Yield (15 Marks)
        # -----------------------------
        if dividend_yield is not None:

            if dividend_yield >= 2:
                score += 15

            elif dividend_yield >= 1:
                score += 10

            elif dividend_yield > 0:
                score += 5

        return score
