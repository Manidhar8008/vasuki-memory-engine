import sqlite3
import pandas as pd

conn = sqlite3.connect("../vasuki.db")

query = """
SELECT
d.title,
COUNT(em.entity_id) as entities
FROM documents d
JOIN entity_mentions em
ON d.id = em.artifact_id
GROUP BY d.id
ORDER BY entities DESC
LIMIT 50
"""

df = pd.read_sql(query, conn)

print(df)
