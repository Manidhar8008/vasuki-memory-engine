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

    sentences = re.split(r'[.!?\n]', text)

    for sentence in sentences:

        sentence = sentence.strip()

        if len(sentence) < 80:
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
            sentence[:1000],
            0.8
        ))

        count += 1

conn.commit()

print("MEMORIES CREATED:", count)

conn.close()
