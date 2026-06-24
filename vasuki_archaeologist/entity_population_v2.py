import sqlite3
import re

DB = "/data/data/com.termux/files/home/vasuki/vasuki.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
SELECT id,content
FROM documents
WHERE content IS NOT NULL
AND length(content) > 100
""")

docs = cur.fetchall()

entity_cache = {}

for doc_id,content in docs:

    words = re.findall(
        r"[A-Za-z][A-Za-z0-9._-]{3,}",
        content
    )

    for word in words:

        entity = word.lower()

        if len(entity) < 4:
            continue

        if entity not in entity_cache:

            cur.execute("""
            INSERT OR IGNORE INTO entities(
                entity,
                entity_type
            )
            VALUES(?,?)
            """,
            (
                entity,
                "concept"
            ))

            cur.execute("""
            SELECT id
            FROM entities
            WHERE entity=?
            """,
            (entity,)
            )

            row = cur.fetchone()

            if row:
                entity_cache[entity] = row[0]

        entity_id = entity_cache.get(entity)

        if entity_id:

            cur.execute("""
            INSERT INTO entity_mentions(
                artifact_id,
                entity_id,
                count
            )
            VALUES(?,?,?)
            """,
            (
                doc_id,
                entity_id,
                1
            ))

conn.commit()
conn.close()

print("DONE")

