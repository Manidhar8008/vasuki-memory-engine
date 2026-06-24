import sqlite3
import re

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

rows = cur.execute("""
SELECT id,entity
FROM entities
""").fetchall()

removed = 0

for eid,entity in rows:

    entity = entity or ""

    if len(entity) < 3:
        cur.execute(
            "DELETE FROM entities WHERE id=?",
            (eid,)
        )
        removed += 1
        continue

    if re.search(r'\d{4,}', entity):
        cur.execute(
            "DELETE FROM entities WHERE id=?",
            (eid,)
        )
        removed += 1
        continue

    if entity.count(".") > 1:
        cur.execute(
            "DELETE FROM entities WHERE id=?",
            (eid,)
        )
        removed += 1
        continue

conn.commit()

print("REMOVED:", removed)

conn.close()
