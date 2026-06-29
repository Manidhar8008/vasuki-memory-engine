import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

cur.execute("""
SELECT id,memory
FROM memories
""")

rows = cur.fetchall()

added = 0

for mid,text in rows:
    text = str(text or "")

keywords = [
    "goal",
    "target",
    "aim",
    "mission",
    "objective",
    "plan"
]

if any(k in text.lower() for k in keywords):

    cur.execute("""
    INSERT INTO goals(
    title,
    status,
    priority,
    created_at
    )
    VALUES(?,?,?,datetime('now'))
    """,(
        text[:200],
        "active",
        1
    ))

    added += 1

conn.commit()

print("GOALS:",added)

conn.close()
