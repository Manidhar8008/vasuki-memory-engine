import sqlite3
from datetime import datetime

DB = "vasuki.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

# ==================================
# MEMORY TABLE
# ==================================

cur.execute("""
CREATE TABLE IF NOT EXISTS memories(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT,
    memory_type TEXT,
    memory TEXT,
    confidence REAL
)
""")

print("\n=== BUILDING MEMORIES ===\n")

# ==================================
# TOP CATEGORIES
# ==================================

cats = cur.execute("""
SELECT category, COUNT(*)
FROM documents
GROUP BY category
ORDER BY COUNT(*) DESC
LIMIT 5
""").fetchall()

for cat,count in cats:

    text = f"{cat} is a dominant domain with {count} documents"

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
        "CATEGORY",
        text,
        0.95
    ))

    print(text)

# ==================================
# TOP CONCEPTS
# ==================================

concepts = cur.execute("""
SELECT concept, frequency
FROM concepts
ORDER BY frequency DESC
LIMIT 10
""").fetchall()

for concept,freq in concepts:

    text = f"Recurring concept: {concept} ({freq} mentions)"

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
        "CONCEPT",
        text,
        0.90
    ))

    print(text)

# ==================================
# RELATIONSHIPS
# ==================================

rels = cur.execute("""
SELECT concept_a, concept_b, weight
FROM relationships
ORDER BY weight DESC
LIMIT 10
""").fetchall()

for a,b,w in rels:

    text = f"{a} often appears with {b} ({w})"

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
        "RELATIONSHIP",
        text,
        0.85
    ))

    print(text)

# ==================================
# STATS MEMORY
# ==================================

doc_count = cur.execute("""
SELECT COUNT(*)
FROM documents
""").fetchone()[0]

char_count = cur.execute("""
SELECT SUM(chars)
FROM documents
""").fetchone()[0]

memory = f"Knowledge base contains {doc_count} documents and {char_count} characters"

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
    "SYSTEM",
    memory,
    1.0
))

print("\n" + memory)

conn.commit()

total = cur.execute("""
SELECT COUNT(*)
FROM memories
""").fetchone()[0]

print(f"\nMEMORIES CREATED: {total}")

conn.close()
