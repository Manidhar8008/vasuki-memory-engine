import sqlite3
from datetime import datetime

DB = "vasuki.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

# ------------------------
# Create observations table
# ------------------------

cur.execute("""
CREATE TABLE IF NOT EXISTS observations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    source TEXT,
    observation TEXT,
    confidence REAL
)
""")

# ------------------------
# Category stats
# ------------------------

categories = cur.execute("""
SELECT category, COUNT(*)
FROM documents
GROUP BY category
ORDER BY COUNT(*) DESC
""").fetchall()

# ------------------------
# Top concepts
# ------------------------

concepts = cur.execute("""
SELECT concept, frequency
FROM concepts
ORDER BY frequency DESC
LIMIT 10
""").fetchall()

# ------------------------
# Top relationships
# ------------------------

relationships = cur.execute("""
SELECT concept_a, concept_b, weight
FROM relationships
ORDER BY weight DESC
LIMIT 10
""").fetchall()

print("\n=== VASUKI OBSERVER ===\n")

# ------------------------
# Categories
# ------------------------

print("CATEGORIES\n")

for cat,count in categories:

    text = f"{cat}: {count}"

    print(text)

    cur.execute("""
    INSERT INTO observations(
        timestamp,
        source,
        observation,
        confidence
    )
    VALUES(?,?,?,?)
    """,(
        datetime.now().isoformat(),
        "classifier",
        text,
        0.95
    ))

# ------------------------
# Concepts
# ------------------------

print("\nTOP CONCEPTS\n")

for concept,freq in concepts:

    text = f"{concept} appears {freq} times"

    print(text)

    cur.execute("""
    INSERT INTO observations(
        timestamp,
        source,
        observation,
        confidence
    )
    VALUES(?,?,?,?)
    """,(
        datetime.now().isoformat(),
        "concepts",
        text,
        0.90
    ))

# ------------------------
# Relationships
# ------------------------

print("\nTOP RELATIONSHIPS\n")

for a,b,w in relationships:

    text = f"{a} ↔ {b} ({w})"

    print(text)

    cur.execute("""
    INSERT INTO observations(
        timestamp,
        source,
        observation,
        confidence
    )
    VALUES(?,?,?,?)
    """,(
        datetime.now().isoformat(),
        "relationships",
        text,
        0.85
    ))

conn.commit()

total = cur.execute("""
SELECT COUNT(*)
FROM observations
""").fetchone()[0]

print("\nObservations stored:", total)

conn.close()
