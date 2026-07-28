from src.utils.database import execute_query

rows = execute_query("PRAGMA foreign_key_check;")

print("=" * 60)

print("FOREIGN KEY CHECK")

print("=" * 60)

if len(rows) == 0:

    print("SUCCESS")
    print("No Foreign Key Errors Found.")

else:

    print("FAILED")

    for row in rows:

        print(row)

print("=" * 60)