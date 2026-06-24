import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

cur.execute("""
SELECT memory
FROM memories
""")

rows = cur.fetchall()

added = 0

for (text,) in rows:
    text = str(text or "")

if any(x in text.lower() for x in [
    "learned",
    "lesson",
    "insight",
    "realized",
    "discovered"
]):

    cur.execute("""
    INSERT INTO learnings(
    learning,
    source,
    created_at
    )
    VALUES(?,?,datetime('now'))
    """,(
        text[:500],
        "memory"
    ))

    added += 1

conn.commit()

print("LEARNINGS:",added)

conn.close()
