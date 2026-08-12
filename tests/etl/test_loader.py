import pandas as pd

from src.etl import loader


def make_files(tmp_path):
    """
    Create all expected dataset files.
    """
    for filename in loader.DATASETS.values():
        (tmp_path / filename).touch()


def fake_read_excel(*args, **kwargs):
    """
    Return a small predictable DataFrame instead of reading real Excel files.
    """
    return pd.DataFrame(
        {
            "company_id": ["TCS", "INFY"],
            "year": [2023, 2024],
            "revenue": [100, 200],
        }
    )


def test_load_all_data_returns_dictionary(tmp_path, monkeypatch):
    make_files(tmp_path)

    monkeypatch.setattr(loader, "RAW_DATA_DIR", tmp_path)
    monkeypatch.setattr(loader.pd, "read_excel", fake_read_excel)

    data = loader.load_all_data()

    assert isinstance(data, dict)


def test_load_all_data_loads_all_datasets(tmp_path, monkeypatch):
    make_files(tmp_path)

    monkeypatch.setattr(loader, "RAW_DATA_DIR", tmp_path)
    monkeypatch.setattr(loader.pd, "read_excel", fake_read_excel)

    data = loader.load_all_data()

    assert len(data) == len(loader.DATASETS)


def test_load_all_data_contains_expected_keys(tmp_path, monkeypatch):
    make_files(tmp_path)

    monkeypatch.setattr(loader, "RAW_DATA_DIR", tmp_path)
    monkeypatch.setattr(loader.pd, "read_excel", fake_read_excel)

    data = loader.load_all_data()

    assert set(data.keys()) == set(loader.DATASETS.keys())


def test_each_dataset_is_dataframe(tmp_path, monkeypatch):
    make_files(tmp_path)

    monkeypatch.setattr(loader, "RAW_DATA_DIR", tmp_path)
    monkeypatch.setattr(loader.pd, "read_excel", fake_read_excel)

    data = loader.load_all_data()

    for df in data.values():
        assert isinstance(df, pd.DataFrame)


def test_each_dataset_has_correct_row_count(tmp_path, monkeypatch):
    make_files(tmp_path)

    monkeypatch.setattr(loader, "RAW_DATA_DIR", tmp_path)
    monkeypatch.setattr(loader.pd, "read_excel", fake_read_excel)

    data = loader.load_all_data()

    for df in data.values():
        assert len(df) == 2


def test_each_dataset_has_expected_columns(tmp_path, monkeypatch):
    make_files(tmp_path)

    monkeypatch.setattr(loader, "RAW_DATA_DIR", tmp_path)
    monkeypatch.setattr(loader.pd, "read_excel", fake_read_excel)

    data = loader.load_all_data()

    expected_columns = [
        "company_id",
        "year",
        "revenue",
    ]

    for df in data.values():
        assert list(df.columns) == expected_columns


def test_missing_file_is_skipped(tmp_path, monkeypatch):
    make_files(tmp_path)

    # Remove one dataset
    missing_file = loader.DATASETS["companies"]
    (tmp_path / missing_file).unlink()

    monkeypatch.setattr(loader, "RAW_DATA_DIR", tmp_path)
    monkeypatch.setattr(loader.pd, "read_excel", fake_read_excel)

    data = loader.load_all_data()

    assert "companies" not in data
    assert len(data) == len(loader.DATASETS) - 1


def test_read_excel_error_is_skipped(tmp_path, monkeypatch):
    make_files(tmp_path)

    def failing_read_excel(*args, **kwargs):
        raise ValueError("Test Excel error")

    monkeypatch.setattr(loader, "RAW_DATA_DIR", tmp_path)
    monkeypatch.setattr(loader.pd, "read_excel", failing_read_excel)

    data = loader.load_all_data()

    assert data == {}


def test_core_datasets_use_header_one(tmp_path, monkeypatch):
    make_files(tmp_path)

    calls = []

    def tracking_read_excel(*args, **kwargs):
        calls.append(kwargs)
        return pd.DataFrame({"A": [1]})

    monkeypatch.setattr(loader, "RAW_DATA_DIR", tmp_path)
    monkeypatch.setattr(loader.pd, "read_excel", tracking_read_excel)

    loader.load_all_data()

    core_datasets = {
        "companies",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "analysis",
        "documents",
        "prosandcons",
    }

    assert sum(1 for call in calls if call.get("header") == 1) == len(core_datasets)


def test_non_core_datasets_use_default_header(tmp_path, monkeypatch):
    make_files(tmp_path)

    calls = []

    def tracking_read_excel(*args, **kwargs):
        calls.append(kwargs)
        return pd.DataFrame({"A": [1]})

    monkeypatch.setattr(loader, "RAW_DATA_DIR", tmp_path)
    monkeypatch.setattr(loader.pd, "read_excel", tracking_read_excel)

    loader.load_all_data()

    non_core_count = len(loader.DATASETS) - 7

    assert sum(1 for call in calls if "header" not in call) == non_core_count
