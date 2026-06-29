import sqlite3
import pandas as pd

DB = "vasuki.db"

conn = sqlite3.connect(DB)

print("\n=== DOCUMENT INVENTORY ===\n")

query = """
SELECT
    id,
    title,
    path,
    chars
FROM documents
ORDER BY chars DESC
LIMIT 100
"""

df = pd.read_sql(query, conn)

print(df.to_string(index=False))

print("\nDocuments:", len(df))

conn.close()
