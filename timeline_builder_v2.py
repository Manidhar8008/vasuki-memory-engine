import sqlite3

conn=sqlite3.connect("vasuki.db")
cur=conn.cursor()

cur.execute("""
DELETE FROM founder_timeline
""")

cur.execute("""
SELECT created_at,memory
FROM memories
LIMIT 1000
""")

for d,m in cur.fetchall():

    cur.execute("""
    INSERT INTO founder_timeline(
    event_date,
    event_type,
    title,
    source,
    importance
    )
    VALUES(
    ?,?,?,?,?
    )
    """,(
        d,
        "memory",
        str(m)[:150],
        "memory",
        1
    ))

conn.commit()

print("TIMELINE BUILT")

conn.close()
