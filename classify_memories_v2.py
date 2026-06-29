import sqlite3

conn=sqlite3.connect("vasuki.db")
cur=conn.cursor()

rows=cur.execute("""
SELECT id,memory
FROM memories
""").fetchall()

for mid,text in rows:

    text=(text or "").lower()

    category="observation"

    if "goal" in text:
        category="goal"

    elif "decision" in text:
        category="decision"

    elif "failed" in text:
        category="failure"

    elif "learned" in text:
        category="learning"

    elif "project" in text:
        category="project"

    cur.execute("""
    UPDATE memories
    SET category=?
    WHERE id=?
    """,(category,mid))

conn.commit()
