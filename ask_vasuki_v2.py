import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

query = input("Ask: ").lower()

rows = cur.execute("""
SELECT title
FROM documents
WHERE LOWER(content) LIKE ?
LIMIT 50
""",(f"%{query}%",)).fetchall()

print("\nFOUND:\n")

for row in rows:
    print(row[0])

conn.close()
