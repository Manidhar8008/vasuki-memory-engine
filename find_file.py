import sqlite3

search = input("Search: ")

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

cur.execute("""
SELECT path
FROM files
WHERE name LIKE ?
LIMIT 20
""", (f"%{search}%",))

results = cur.fetchall()

for r in results:
    print(r[0])

conn.close()
