import sqlite3
import re

DB = "vasuki.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

try:
    cur.execute("""
    ALTER TABLE entities
    ADD COLUMN quality_score REAL DEFAULT 0
    """)
except:
    pass

cur.execute("""
SELECT id,entity
FROM entities
""")

rows = cur.fetchall()

updated = 0

for eid, entity in rows:

    text = str(entity or "").strip().lower()

    score = 0

    if len(text) >= 4:
        score += 2

    if len(text) >= 8:
        score += 2

    if re.search(r'[a-z]', text):
        score += 2

    if re.search(r'^[a-z]+$', text):
        score += 3

    if "." in text:
        score -= 2

    if "_" in text:
        score -= 2

    if len(re.findall(r'\d', text)) > 2:
        score -= 3

    if len(text) < 3:
        score -= 5

    if text.startswith("a."):
        score -= 5

    if text.startswith("aa"):
        score -= 3

    if text.endswith("."):
        score -= 2

    cur.execute("""
    UPDATE entities
    SET quality_score=?
    WHERE id=?
    """,(score,eid))

    updated += 1

conn.commit()

print("RANKED:",updated)

cur.execute("""
SELECT entity,quality_score
FROM entities
ORDER BY quality_score DESC
LIMIT 50
""")

print("\nTOP ENTITIES\n")

for row in cur.fetchall():
    print(row)

conn.close()
