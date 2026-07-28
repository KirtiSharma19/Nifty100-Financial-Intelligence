from src.etl.database_loader import DatabaseLoader

db = DatabaseLoader()

db.create_database()

db.load_data()