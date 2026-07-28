from src.services.ratio_engine import DatasetBuilder


class SectorDashboard:

    def sector_scores(self):

        engine = RatioEngine()

        df = engine.build_dataset()

        sector_score = (
            df.groupby("broad_sector")["quality_score"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )

        return sector_score