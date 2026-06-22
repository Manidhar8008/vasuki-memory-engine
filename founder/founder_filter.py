import sqlite3

conn = sqlite3.connect("founder.db")
cur = conn.cursor()

KEYWORDS = [
    "vasuki",
    "mw",
    "janani",
    "agent",
    "architecture",
    "research",
    "vision",
    "roadmap",
    "prompt",
    "strategy",
    "memory"
]

for k in KEYWORDS:

    print(f"\n=== {k.upper()} ===")

    cur.execute("""
    SELECT filename,path
    FROM founder_artifacts
    WHERE lower(filename) LIKE ?
    LIMIT 20
    """,(f"%{k}%",))

    rows = cur.fetchall()

    for row in rows:
        print(row[0])

conn.close()
