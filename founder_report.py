import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

tables = [
    "documents",
    "memories",
    "entities",
    "goals",
    "projects",
    "decisions",
    "failures",
    "learnings"
]

print("\n=== VASUKI FOUNDER DASHBOARD ===\n")

for t in tables:

    try:
        count = cur.execute(
            f"SELECT COUNT(*) FROM {t}"
        ).fetchone()[0]

        print(f"{t:15} {count}")

    except:
        pass

print("\nTOP ENTITIES\n")

rows = cur.execute("""
SELECT entity,
       COUNT(*) as c
FROM entities
GROUP BY entity
ORDER BY c DESC
LIMIT 20
""").fetchall()

for r in rows:
    print(r)

conn.close()
