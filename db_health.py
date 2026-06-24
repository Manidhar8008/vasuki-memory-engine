import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

tables = cur.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""").fetchall()

print("\n=== TABLES ===\n")

for t in tables:
    print(t[0])

conn.close()
