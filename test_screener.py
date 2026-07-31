from src.screener.engine import ScreenerEngine

engine = ScreenerEngine()

presets = {
    "Quality Compounder": engine.quality_compounder(),
    "Value Pick": engine.value_pick(),
    "Growth Accelerator": engine.growth_accelerator(),
    "Dividend Champion": engine.dividend_champion(),
    "Debt Free Blue Chip": engine.debt_free_bluechip(),
    "Turnaround Watch": engine.turnaround_watch(),
}

for name, df in presets.items():

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    print("Companies :", len(df))

    print(
        df[
            [
                "company_name",
                "quality_score",
                "return_on_equity_pct",
                "debt_to_equity",
            ]
        ].head()
    )