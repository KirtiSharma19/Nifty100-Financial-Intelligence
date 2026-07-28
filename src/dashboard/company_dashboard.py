from src.services.ratio_engine import RatioEngine


class CompanyDashboard:

    def top_quality_companies(self):

        engine = RatioEngine()

        df = engine.build_dataset()

        top = (
            df.sort_values(
                "quality_score",
                ascending=False
            )
            .drop_duplicates("company_id")
            .head(10)
        )

        return top[
            [
                "company_id",
                "quality_score"
            ]
        ]