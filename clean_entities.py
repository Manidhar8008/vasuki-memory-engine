import sqlite3
import re

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

cur.execute("""
SELECT id,entity
FROM entities
""")

rows = cur.fetchall()

removed = 0

for eid,name in rows:

    if len(name) < 3:
        cur.execute(
            "DELETE FROM entities WHERE id=?",
            (eid,)
        )
        removed += 1
        continue

    if re.search(r'[^a-zA-Z0-9 ._-]',name):
        cur.execute(
            "DELETE FROM entities WHERE id=?",
            (eid,)
        )
        removed += 1

conn.commit()

print("REMOVED:",removed)

conn.close()
