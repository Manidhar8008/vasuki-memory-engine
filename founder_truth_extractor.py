import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

TRUTHS = [
    "vasuki",
    "janani",
    "mw.ai",
    "local-first",
    "architecture",
    "founder",
    "goal",
    "decision",
    "failure",
    "learning",
    "remote job",
    "cto",
    "mrr"
]

for keyword in TRUTHS:

    cur.execute("""
    SELECT memory
    FROM memories
    WHERE lower(memory) LIKE ?
    LIMIT 20
    """, (f"%{keyword}%",))

    rows = cur.fetchall()

    print("\n" + "="*80)
    print(keyword.upper())
    print("="*80)

    for row in rows:
        print("-", row[0][:300])

conn.close()
