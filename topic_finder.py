import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

rows = cur.execute("""
SELECT concept, frequency
FROM concepts
ORDER BY frequency DESC
LIMIT 30
""").fetchall()

print("\nTOP THEMES\n")

for concept, freq in rows:
    print(f"{concept}: {freq}")

conn.close()

