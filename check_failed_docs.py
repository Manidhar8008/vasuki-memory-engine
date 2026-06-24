import sqlite3
from pathlib import Path

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

rows = cur.execute("""
SELECT id,title,path
FROM documents
WHERE chars=0
LIMIT 100
""").fetchall()

print("\nFAILED DOCS\n")

for doc_id,title,path in rows:
    exists = Path(path).exists()
    print(f"{doc_id} | {exists} | {title}")

conn.close()
