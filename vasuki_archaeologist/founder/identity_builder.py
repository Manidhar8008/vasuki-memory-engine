import sqlite3

DB="founder.db"

ENTITIES=[
    "MANIDHAR",
    "MW.AI",
    "JANANI",
    "VASUKI"
]

conn=sqlite3.connect(DB)
cur=conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS entity_mentions(
id INTEGER PRIMARY KEY,
entity_name TEXT,
source_file TEXT,
evidence TEXT,
confidence REAL,
created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

rows=cur.execute("""
SELECT filename
FROM founder_artifacts
""").fetchall()

for row in rows:

    filename=str(row[0])

    upper=filename.upper()

    for entity in ENTITIES:

        if entity in upper:

            cur.execute("""
            INSERT INTO entity_mentions(
            entity_name,
            source_file,
            evidence,
            confidence
            )
            VALUES(?,?,?,?)
            """,
            (
                entity,
                filename,
                filename,
                0.90
            ))

conn.commit()

print("IDENTITY GRAPH BUILT")
