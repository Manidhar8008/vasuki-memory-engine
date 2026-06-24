import sqlite3
from collections import Counter
import re

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

cur.execute("DELETE FROM graph")

rows = cur.execute("""
SELECT content
FROM documents
LIMIT 200
""").fetchall()

for row in rows:

    text = row[0].lower()

    words = re.findall(r"\b[a-z]{4,}\b", text)

    words = words[:200]

    for i in range(len(words)-1):

        a = words[i]
        b = words[i+1]

        if a == b:
            continue

        cur.execute("""
        INSERT INTO graph(source,target,weight)
        VALUES(?,?,1)
        """,(a,b))

conn.commit()
conn.close()

print("GRAPH CREATED")

