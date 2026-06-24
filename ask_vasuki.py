import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

query = input("Ask Vasuki: ")

rows = cur.execute("""
SELECT title
FROM documents
WHERE content LIKE ?
LIMIT 20
""", (f"%{query}%",)).fetchall()

for row in rows:
    print(row[0])

conn.close()

