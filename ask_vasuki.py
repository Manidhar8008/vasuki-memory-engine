import sqlite3
import sys

DB = "/data/data/com.termux/files/home/vasuki/vasuki.db"

query = " ".join(sys.argv[1:]).lower()

conn = sqlite3.connect(DB)
cur = conn.cursor()

print("\n=== VASUKI ===\n")

# Search timeline
cur.execute("""
SELECT title, content
FROM timeline
WHERE lower(title) LIKE ?
OR lower(content) LIKE ?
LIMIT 20
""",
(
    f"%{query}%",
    f"%{query}%"
))

rows = cur.fetchall()

if rows:

    print("TIMELINE EVIDENCE\n")

    for title, content in rows:

        print(f"[{title}]")
        print(content)
        print()

# Search documents
cur.execute("""
SELECT title
FROM documents
WHERE lower(content) LIKE ?
LIMIT 20
""",
(
    f"%{query}%",
))

docs = cur.fetchall()

if docs:

    print("DOCUMENTS\n")

    for d in docs:

        print("-", d[0])

if not rows and not docs:

    print("No evidence found.")

conn.close()
