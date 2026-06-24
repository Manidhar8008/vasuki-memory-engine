import sqlite3
import sys

query=sys.argv[1].lower()

conn=sqlite3.connect("vasuki.db")
cur=conn.cursor()

print("\n=== MEMORIES ===\n")

rows=cur.execute("""
SELECT memory
FROM memories
WHERE memory LIKE ?
LIMIT 20
""",(f"%{query}%",)).fetchall()

for r in rows:
    print("-",r[0][:250])

print("\n=== GOALS ===\n")

rows=cur.execute("""
SELECT title,status
FROM goals
WHERE title LIKE ?
LIMIT 10
""",(f"%{query}%",)).fetchall()

for r in rows:
    print(r)

print("\n=== DECISIONS ===\n")

rows=cur.execute("""
SELECT decision
FROM decisions
WHERE decision LIKE ?
LIMIT 10
""",(f"%{query}%",)).fetchall()

for r in rows:
    print("-",r[0])
