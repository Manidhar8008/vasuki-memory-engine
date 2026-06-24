import sqlite3
from datetime import datetime

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

try:
    cur.execute("""
    ALTER TABLE entities
    ADD COLUMN frequency INTEGER DEFAULT 0
    """)
except:
    pass

try:
    cur.execute("""
    ALTER TABLE entities
    ADD COLUMN created_at TEXT
    """)
except:
    pass

cur.execute("""
SELECT id, entity
FROM entities
""")

rows = cur.fetchall()

for entity_id, entity in rows:

    cur.execute("""
    SELECT COUNT(*)
    FROM documents
    WHERE content LIKE ?
    """, (f"%{entity}%",))

    count = cur.fetchone()[0]

    cur.execute("""
    UPDATE entities
    SET frequency=?
    WHERE id=?
    """,(count,entity_id))

conn.commit()

print("ENTITY FREQUENCIES BUILT")

conn.close()
