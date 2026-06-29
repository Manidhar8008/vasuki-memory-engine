import sqlite3
import re
from collections import Counter

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

rows = cur.execute("""
SELECT content
FROM documents
""").fetchall()

words = []

for row in rows:

    text = row[0] or ""

    found = re.findall(
        r"\b[a-zA-Z]{4,}\b",
        text.lower()
    )

    words.extend(found)

counter = Counter(words)

print("\nTOP CONCEPTS\n")

for word,count in counter.most_common(50):
    print(word,count)

conn.close()
