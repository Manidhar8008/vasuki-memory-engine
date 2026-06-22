import sqlite3

conn = sqlite3.connect(
    "vasuki.db"
)

cur = conn.cursor()

cur.execute("""
SELECT *
FROM events
ORDER BY created_at
""")

rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()
