import sqlite3
from collections import Counter
import re

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

rows = cur.execute("""
SELECT title, content
FROM documents
""").fetchall()

all_words = []

for title, content in rows:
    if not content:
        continue

    words = re.findall(r"\b[a-zA-Z]{4,}\b", content.lower())
    all_words.extend(words)

counter = Counter(all_words)

print("\nTOP WORDS\n")

for word, count in counter.most_common(50):
    print(f"{word}: {count}")

conn.close()
