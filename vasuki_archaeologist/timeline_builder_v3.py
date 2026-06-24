import sqlite3

DB = "/data/data/com.termux/files/home/vasuki/vasuki.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

KEYWORDS = [
    "manidhar",
    "mw.ai",
    "mw ai",
    "vasuki",
    "janani",
    "room os"
]

cur.execute("""
SELECT id,title,content
FROM documents
WHERE content IS NOT NULL
""")

for doc_id,title,content in cur.fetchall():

    text = content.lower()

    for keyword in KEYWORDS:

        if keyword in text:

            cur.execute("""
            INSERT INTO timeline(
                source,
                title,
                timestamp,
                content
            )
            VALUES(
                ?,
                ?,
                datetime('now'),
                ?
            )
            """,
            (
                "document",
                keyword.upper(),
                title
            ))

conn.commit()
conn.close()

print("TIMELINE BUILT")
