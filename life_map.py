import sqlite3
from collections import Counter

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

rows = cur.execute("""
SELECT path
FROM files
""").fetchall()

folders = Counter()

for (path,) in rows:

    if not path:
        continue

    parts = path.split("/")

    if len(parts) > 4:
        folders[parts[4]] += 1

print("\n=== LIFE MAP ===\n")

for name,count in folders.most_common(30):
    print(f"{name:<25} {count}")

conn.close()
