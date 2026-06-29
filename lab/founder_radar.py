import sqlite3
import pandas as pd

conn = sqlite3.connect("../vasuki.db")

docs = pd.read_sql("""
SELECT
project,
COUNT(*) as total
FROM document_identity
GROUP BY project
ORDER BY total DESC
""", conn)

print("\nPROJECTS\n")
print(docs)
