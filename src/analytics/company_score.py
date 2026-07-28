class CompanyScore:

    @staticmethod
    def score(roe, debt, margin):

        score = 0

        if roe > 20:
            score += 40
        elif roe > 15:
            score += 30
        elif roe > 10:
            score += 20

        if debt < 1:
            score += 30
        elif debt < 2:
            score += 20

        if margin > 20:
            score += 30
        elif margin > 10:
            score += 20

        return score