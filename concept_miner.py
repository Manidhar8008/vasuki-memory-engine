import sqlite3
import re
from collections import Counter

DB = "vasuki.db"

STOP_WORDS = {
    "the","and","for","with","that","this","from","into",
    "have","has","are","was","were","you","your","their",
    "will","can","could","should","would","about","after",
    "before","then","than","been","being","also","such",
    "there","here","they","them","our","his","her","its",
    "not","but","all","any","more","most","other","some",
    "each","many","much","very","what","when","where",
    "which","while","who","why","how"
}

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS concepts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept TEXT UNIQUE,
    frequency INTEGER
)
""")

print("Reading documents...")

cur.execute("SELECT content FROM documents")
rows = cur.fetchall()

counter = Counter()

for row in rows:

    text = str(row[0]).lower()

    words = re.findall(r"\b[a-z]{4,20}\b", text)

    for word in words:

        if word in STOP_WORDS:
            continue

        counter[word] += 1

print("Found concepts:", len(counter))

for concept, freq in counter.most_common(5000):

    cur.execute("""
    INSERT OR REPLACE INTO concepts(
        concept,
        frequency
    )
    VALUES(?,?)
    """, (concept, freq))

conn.commit()

print("\nTOP 50 CONCEPTS\n")

for concept, freq in counter.most_common(50):
    print(f"{concept}: {freq}")

conn.close()

print("\nDONE")
