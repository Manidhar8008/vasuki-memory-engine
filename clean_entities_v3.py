import sqlite3
import re

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

cur.execute("""
SELECT id,entity,quality_score
FROM entities
""")

rows = cur.fetchall()

removed = 0

for eid,name,score in rows:

    text = str(name or "").strip().lower()

    bad = False

    if score < 0:
        bad = True

    if len(text) < 3:
        bad = True

    if re.match(r'^[0-9]+$', text):
        bad = True

    if re.match(r'^[a-z]\.$', text):
        bad = True

    if text.startswith("a."):
        bad = True

    if text.startswith("aa"):
        bad = True

    if len(re.findall(r'\d', text)) > 4:
        bad = True

    if bad:
        cur.execute(
            "DELETE FROM entities WHERE id=?",
            (eid,)
        )
        removed += 1

conn.commit()

print("REMOVED:",removed)

conn.close()
