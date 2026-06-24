import sqlite3
import re

DB = "/data/data/com.termux/files/home/vasuki/vasuki.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS timeline (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    event TEXT,
    source TEXT
)
""")

KEYWORDS = [
    "manidhar",
    "mw.ai",
    "mw ai",
    "vasuki",
    "janani",
    "room os"
]

cur.execute("""
SELECT id,title,path,content
FROM documents
""")

for doc_id,title,path,content in cur.fetchall():

    text = (content or "").lower()

    for keyword in KEYWORDS:

        if keyword in text:

            cur.execute("""
            INSERT INTO timeline(
                timestamp,
                event,
                source
            )
            VALUES(
                datetime('now'),
                ?,
                ?
            )
            """,
            (
                f"Mentioned: {keyword}",
                title
            ))

conn.commit()
conn.close()

print("Timeline Built")
