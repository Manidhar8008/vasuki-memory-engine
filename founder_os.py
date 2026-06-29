import sqlite3
from collections import Counter

DB="vasuki.db"

conn=sqlite3.connect(DB)
cur=conn.cursor()

print("\n=== VASUKI FOUNDER OS ===\n")

tables = [
    "documents",
    "memories",
    "entities",
    "goals",
    "decisions",
    "learnings",
    "failures"
]

for t in tables:

    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        c=cur.fetchone()[0]
        print(f"{t:<15} {c}")
    except:
        pass

print("\n=== TOP PROJECTS ===\n")

PROJECTS=[
    "vasuki",
    "janani",
    "mw.ai",
    "aim1000",
    "founder corpus"
]

cur.execute("""
SELECT memory
FROM memories
""")

rows=cur.fetchall()

project_counter=Counter()

for row in rows:

    text=str(row[0]).lower()

    for p in PROJECTS:

        if p in text:
            project_counter[p]+=1

for k,v in project_counter.most_common():
    print(k,v)

print("\n=== TOP FAILURES ===\n")

cur.execute("""
SELECT failure
FROM failures
LIMIT 10
""")

for row in cur.fetchall():
    print("-",str(row[0])[:120])

print("\n=== TOP LEARNINGS ===\n")

cur.execute("""
SELECT learning
FROM learnings
LIMIT 10
""")

for row in cur.fetchall():
    print("-",str(row[0])[:120])

print("\n=== TOP GOALS ===\n")

cur.execute("""
SELECT title
FROM goals
LIMIT 10
""")

for row in cur.fetchall():
    print("-",str(row[0])[:120])

conn.close()
