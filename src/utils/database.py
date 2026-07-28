import sqlite3
from src.utils.paths import DATABASE_FILE


def get_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn