import sqlite3
import re

DB = "vasuki.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

entities = set()

cur.execute(
    "SELECT content FROM documents"
)

for row in cur.fetchall():

    text = row[0]

    matches = re.findall(
        r'\b[A-Z][A-Za-z0-9_-]+\b',
        text
    )

    for m in matches:
        entities.add(m)

for e in sorted(entities):
    print(e)

conn.close()
