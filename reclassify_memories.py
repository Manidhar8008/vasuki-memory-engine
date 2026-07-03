import sqlite3
import re
from collections import Counter

DB = "vasuki.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS classified_memories(
    id INTEGER PRIMARY KEY,
    memory_id INTEGER,
    category TEXT,
    confidence REAL,
    content TEXT
)
""")

PROJECT_PATTERNS = [
    r'capstone',
    r'project',
    r'platform',
    r'system',
    r'roadmap',
    r'vasuki',
    r'janani',
    r'lime'
]

SKILL_PATTERNS = [
    r'python',
    r'fastapi',
    r'react',
    r'typescript',
    r'sql',
    r'sqlite',
    r'postgres',
    r'git',
    r'github',
    r'llm',
    r'ai',
    r'rag',
    r'machine learning'
]

COMPANY_PATTERNS = [
    r'cognizant',
    r'genpact',
    r'openai',
    r'google',
    r'microsoft',
    r'lime'
]

GOAL_PATTERNS = [
    r'goal',
    r'build',
    r'launch',
    r'create',
    r'grow',
    r'roadmap'
]

DECISION_PATTERNS = [
    r'decided',
    r'decision',
    r'choose',
    r'should'
]

def classify(text):
    t = text.lower()

    scores = Counter()

    for p in PROJECT_PATTERNS:
        if re.search(p, t):
            scores["project"] += 1

    for p in SKILL_PATTERNS:
        if re.search(p, t):
            scores["skill"] += 1

    for p in COMPANY_PATTERNS:
        if re.search(p, t):
            scores["company"] += 1

    for p in GOAL_PATTERNS:
        if re.search(p, t):
            scores["goal"] += 1

    for p in DECISION_PATTERNS:
        if re.search(p, t):
            scores["decision"] += 1

    if not scores:
        return "observation", 0.5

    cat = scores.most_common(1)[0][0]
    conf = min(1.0, scores[cat] / 3.0)

    return cat, conf

cur.execute("SELECT id,memory FROM memories")

batch = []

for mid, memory in cur.fetchall():
    category, confidence = classify(memory or "")

    batch.append(
        (mid, category, confidence, memory)
    )

cur.executemany("""
INSERT INTO classified_memories(
    memory_id,
    category,
    confidence,
    content
)
VALUES(?,?,?,?)
""", batch)

conn.commit()

print(f"Processed {len(batch)} memories")

for row in cur.execute("""
SELECT category, COUNT(*)
FROM classified_memories
GROUP BY category
ORDER BY COUNT(*) DESC
"""):
    print(row)

conn.close()
