import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

rows = cur.execute("""
SELECT memory
FROM memories
LIMIT 50
""").fetchall()

for row in rows:
    print("\n---")
    print(row[0][:300])

conn.close()
