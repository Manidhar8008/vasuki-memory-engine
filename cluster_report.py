import sqlite3
import pandas as pd

conn = sqlite3.connect("vasuki.db")

df = pd.read_sql("""
SELECT cluster,
COUNT(*) total
FROM document_clusters
GROUP BY cluster
ORDER BY total DESC
""", conn)

print(df)

conn.close()

