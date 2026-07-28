from src.etl.loader import load_all_data
from src.etl.validator import DataValidator

datasets = load_all_data()

validator = DataValidator()

validator.validate(datasets)