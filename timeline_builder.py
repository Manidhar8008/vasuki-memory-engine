import sqlite3
import pandas as pd

DB = "vasuki.db"

conn = sqlite3.connect(DB)

print("\n=== TIMELINE ===\n")

tables = pd.read_sql(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    """,
    conn
)

available = tables["name"].tolist()

if "timeline" in available:

    df = pd.read_sql(
        """
        SELECT *
        FROM timeline
        LIMIT 200
        """,
        conn
    )

    print(df.to_string(index=False))

else:
    print("timeline table not found")

conn.close()
