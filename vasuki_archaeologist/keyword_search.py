import sqlite3
import sys

DB = "vasuki.db"

keyword = sys.argv[1].lower()

conn = sqlite3.connect(DB)
cur = conn.cursor()

tables = [
    "documents",
    "memories",
    "observations"
]

for table in tables:

    try:
        cur.execute(
            f"SELECT * FROM {table}"
        )

        rows = cur.fetchall()

        for row in rows:

            text = str(row).lower()

            if keyword in text:

                print("\n")
                print("="*50)
                print(table)
                print(row)

    except Exception:
        pass

conn.close()
