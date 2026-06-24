import sqlite3
import re
from itertools import combinations
from collections import Counter

DB = "vasuki.db"

TRACKED = {
    "agent",
    "agents",
    "memory",
    "rag",
    "retrieval",
    "vector",
    "embedding",
    "llm",
    "prompt",
    "automation",
    "workflow",
    "database",
    "sql",
    "python",
    "model",
    "models",
    "knowledge",
    "context"
}

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("DELETE FROM relationships")

rows = cur.execute(
    "SELECT content FROM documents"
).fetchall()

pairs = Counter()

for row in rows:

    text = str(row[0]).lower()

    words = set(
        re.findall(r"\b[a-z]{3,20}\b", text)
    )

    found = words.intersection(TRACKED)

    for a, b in combinations(sorted(found), 2):
        pairs[(a, b)] += 1

for (a, b), weight in pairs.items():

    cur.execute("""
    INSERT INTO relationships(
        concept_a,
        concept_b,
        weight
    )
    VALUES (?, ?, ?)
    """, (a, b, weight))

conn.commit()

print("Relationships:", len(pairs))

conn.close()
