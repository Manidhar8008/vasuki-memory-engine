import sqlite3
from collections import Counter
import re

db = sqlite3.connect("vasuki.db")
cur = db.cursor()

rows = cur.execute("""
SELECT description
FROM ontology_objects
""").fetchall()

words = []

for r in rows:
    text = str(r[0]).lower()

    for w in re.findall(r"[a-zA-Z]{5,}", text):
        words.append(w)

counter = Counter(words)

print("\n=== TOP PATTERNS ===\n")

for word,count in counter.most_common(50):
    print(word,count)
