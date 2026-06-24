import sqlite3
import re
from datetime import datetime

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

cur.execute("""
SELECT content
FROM documents
WHERE content IS NOT NULL
""")

rows = cur.fetchall()

count = 0

for row in rows:

    text = row[0]

    chunks = re.split(r'[.!?\n]', text)

    for chunk in chunks:

        chunk = chunk.strip()

        if len(chunk) < 100:
            continue

        cur.execute("""
        INSERT INTO memories(
            created_at,
            memory_type,
            memory,
            confidence
        )
        VALUES(?,?,?,?)
        """,(
            datetime.now().isoformat(),
            "document_memory",
            chunk[:1500],
            0.8
        ))

        count += 1

conn.commit()

print("MEMORIES:",count)

conn.close()
