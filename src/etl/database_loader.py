#Creates SQLite database and executes schema.sql
import sqlite3
from pathlib import Path
from src.utils.paths import DATABASE_FILE, BASE_DIR
import pandas as pd
from src.etl.loader import load_all_data


class DatabaseLoader:

    def __init__(self):
        self.database = DATABASE_FILE
        self.schema = BASE_DIR / "db" / "schema.sql"

    def create_database(self):

        print("=" * 60)
        print("Creating SQLite Database...")
        print("=" * 60)

        conn = sqlite3.connect(self.database)

        conn.execute("PRAGMA foreign_keys = ON;")

        with open(self.schema, "r", encoding="utf-8") as sql_file:
            conn.executescript(sql_file.read())

        conn.commit()
        conn.close()

        print(f"[SUCCESS] Database Created : {self.database}")

    def load_data(self):

        datasets = load_all_data()

        conn = sqlite3.connect(self.database)

        print("\nLoading Tables Into SQLite...\n")

        for table_name, df in datasets.items():

            df.to_sql(
                table_name,
                conn,
                if_exists="replace",
                index=False
            )

            print(
                f"[OK] {table_name:<20}"
                f"Rows : {len(df)}"
            )

        conn.commit()

        conn.close()

        print("\nAll Tables Loaded Successfully.")

if __name__ == "__main__":

    DatabaseLoader().create_database()