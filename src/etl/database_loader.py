#Creates SQLite database and executes schema.sql

import sqlite3
from pathlib import Path

from src.utils.paths import DATABASE_FILE, BASE_DIR


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


if __name__ == "__main__":

    DatabaseLoader().create_database()