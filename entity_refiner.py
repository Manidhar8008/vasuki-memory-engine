import sqlite3

DB = "/data/data/com.termux/files/home/vasuki/vasuki.db"

STOPWORDS = {
    "with","that","your","from","shall","this",
    "which","will","have","such","other",
    "what","when","they","their","into",
    "after","same","used","also","more",
    "been","where","under"
}

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
SELECT id,entity
FROM entities
""")

rows = cur.fetchall()

deleted = 0

for entity_id,entity in rows:

    if entity.lower() in STOPWORDS:

        cur.execute("""
        DELETE FROM entities
        WHERE id=?
        """,(entity_id,))

        deleted += 1

conn.commit()

print(
    f"Deleted {deleted} stopwords"
)

conn.close()
