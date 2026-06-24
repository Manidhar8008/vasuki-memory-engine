import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

rows = cur.execute("""
SELECT created_at,memory
FROM memories
ORDER BY created_at DESC
LIMIT 100
""").fetchall()

print("\n=== TIMELINE ===\n")

for date,text in rows:
    print(f"[{date}] {text[:150]}")
    print()
