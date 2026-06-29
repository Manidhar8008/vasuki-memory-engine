import sqlite3
import sys

query = " ".join(sys.argv[1:]).lower()

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

print("\n=== MEMORIES ===\n")

rows = cur.execute("""
SELECT memory
FROM memories
WHERE memory LIKE ?
LIMIT 20
""",("%"+query+"%",)).fetchall()

for r in rows:
    print(r[0])
    print()

print("\n=== GOALS ===\n")

try:
    rows = cur.execute("""
    SELECT title
    FROM goals
    WHERE title LIKE ?
    LIMIT 20
    """,("%"+query+"%",)).fetchall()

    for r in rows:
        print(r[0])

except:
    pass

print("\n=== DECISIONS ===\n")

try:
    rows = cur.execute("""
    SELECT decision
    FROM decisions
    WHERE decision LIKE ?
    LIMIT 20
    """,("%"+query+"%",)).fetchall()

    for r in rows:
        print(r[0])

except:
    pass

conn.close()
