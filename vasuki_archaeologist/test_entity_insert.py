import sqlite3

DB = "/data/data/com.termux/files/home/vasuki/vasuki.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
INSERT INTO entities(
entity,
entity_type
)
VALUES(
'VASUKI_TEST',
'test'
)
""")

conn.commit()

cur.execute("""
SELECT *
FROM entities
WHERE entity='VASUKI_TEST'
""")

print(cur.fetchall())

conn.close()
