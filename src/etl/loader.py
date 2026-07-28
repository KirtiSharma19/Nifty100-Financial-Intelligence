import pandas as pd
from pathlib import Path
from src.utils.paths import RAW_DATA_DIR

# List of all datasets
DATASETS = {
    "companies": "companies.xlsx",
    "profitandloss": "profitandloss.xlsx",
    "balancesheet": "balancesheet.xlsx",
    "cashflow": "cashflow.xlsx",
    "analysis": "analysis.xlsx",
    "documents": "documents.xlsx",
    "prosandcons": "prosandcons.xlsx",
    "financial_ratios": "financial_ratios.xlsx",
    "market_cap": "market_cap.xlsx",
    "peer_groups": "peer_groups.xlsx",
    "sectors": "sectors.xlsx",
    "stock_prices": "stock_prices.xlsx"
}


def load_all_data():
    """
    Load all Excel datasets into a dictionary.
    Returns:
        dict[str, pd.DataFrame]
    """

    data = {}

    print("=" * 60)
    print("Loading Nifty100 Datasets...")
    print("=" * 60)

    for name, file in DATASETS.items():

        file_path = RAW_DATA_DIR / file

        if not file_path.exists():
            print(f"[ERROR] Missing File : {file}")
            continue

        try:

            # Core datasets
            if name in [
                "companies",
                "profitandloss",
                "balancesheet",
                "cashflow",
                "analysis",
                "documents",
                "prosandcons"
            ]:
                df = pd.read_excel(file_path, header=1)

            else:
                df = pd.read_excel(file_path)

            data[name] = df

            print(
                f"[OK] {name:<20}"
                f" Rows: {df.shape[0]:<6}"
                f" Columns: {df.shape[1]}"
            )

        except Exception as e:
            print(f"[FAILED] {file}")
            print(e)

    print("=" * 60)
    print("Datasets Loaded :", len(data))
    print("=" * 60)

    return data


if __name__ == "__main__":

    datasets = load_all_data()