import sqlite3
from collections import Counter
import os

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

print("\n=== VASUKI ARCHAEOLOGIST ===\n")

# Extensions
print("TOP FILE TYPES")
rows = cur.execute("""
SELECT extension, COUNT(*)
FROM files
GROUP BY extension
ORDER BY COUNT(*) DESC
LIMIT 15
""").fetchall()

for ext, count in rows:
    print(f"{ext}: {count}")

print("\nTOP FOLDERS")

folders = Counter()

rows = cur.execute("""
SELECT path
FROM files
""").fetchall()

for (path,) in rows:
    if path:
        parts = path.split("/")
        if len(parts) > 0:
            folders[parts[-1]] += 1

for folder, count in folders.most_common(20):
    print(f"{folder}: {count}")

conn.close()
