from src.services.ratio_engine import DatasetBuilder


def main():

    print("=" * 60)
    print("NIFTY100 FINANCIAL INTELLIGENCE")
    print("=" * 60)

    engine = DatasetBuilder()

    df = engine.build_dataset()

    print()
    print("Dataset Loaded Successfully")
    print(f"Total Records   : {len(df)}")
    print(f"Total Companies : {df['company_name'].nunique()}")

    print()
    print("Top 5 Records")
    print(df.head())


if __name__ == "__main__":
    main()