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
    "decided",
    "decision",
    "choose",
    "chosen",
    "selected"
]):

    cur.execute("""
    INSERT INTO decisions(
    decision,
    reason,
    impact,
    created_at
    )
    VALUES(?,?,?,datetime('now'))
    """,(
        text[:300],
        "",
        ""
    ))

    added += 1

conn.commit()

print("DECISIONS:",added)

conn.close()
