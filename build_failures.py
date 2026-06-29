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
    "failed",
    "failure",
    "mistake",
    "wrong",
    "lost"
]):

    cur.execute("""
    INSERT INTO failures(
    failure,
    lesson,
    created_at
    )
    VALUES(?,?,datetime('now'))
    """,(
        text[:500],
        ""
    ))

    added += 1

conn.commit()

print("FAILURES:",added)

conn.close()
