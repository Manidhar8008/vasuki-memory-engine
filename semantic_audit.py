#!/usr/bin/env python3

import sqlite3
import json
from pathlib import Path

DB = str(Path.home() / "vasuki" / "vasuki.db")

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# --------------------------------------------------
# CREATE TABLE
# --------------------------------------------------

cur.execute("""
CREATE TABLE IF NOT EXISTS canonical_entities(
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    entity_type TEXT,
    frequency INTEGER,
    confidence REAL,
    evidence_count INTEGER
)
""")

conn.commit()

# --------------------------------------------------
# CLASSIFIERS
# --------------------------------------------------

TECH_WORDS = {
    "python","fastapi","postgresql","sqlite",
    "react","typescript","javascript",
    "docker","kubernetes","ollama",
    "qdrant","github","git","linux",
    "llm","rag","openai","gemini"
}

COMPANY_WORDS = {
    "cognizant",
    "genpact",
    "lime",
    "google",
    "microsoft",
    "amazon",
    "openai"
}

PROJECT_WORDS = {
    "vasuki",
    "janani",
    "mw.ai",
    "startup broadcasting system",
    "lime micromobility"
}

PERSON_WORDS = {
    "manidhar"
}


def classify(name):

    n = str(name).strip().lower()

    if n in PERSON_WORDS:
        return "PERSON", 0.95

    if n in COMPANY_WORDS:
        return "COMPANY", 0.90

    if n in PROJECT_WORDS:
        return "PROJECT", 0.90

    if n in TECH_WORDS:
        return "TECHNOLOGY", 0.90

    if len(n.split()) <= 3 and any(
        x in n for x in [
            "python",
            "sql",
            "ml",
            "ai",
            "engineering",
            "analytics",
            "data"
        ]
    ):
        return "SKILL", 0.70

    return "OTHER", 0.30


# --------------------------------------------------
# LOAD ENTITIES
# --------------------------------------------------

cur.execute("""
SELECT
    entity,
    frequency
FROM entities
ORDER BY frequency DESC
LIMIT 5000
""")

rows = cur.fetchall()

stats = {}

for row in rows:

    name = row["entity"]
    freq = row["frequency"]

    etype, conf = classify(name)

    stats[etype] = stats.get(etype, 0) + 1

    cur.execute("""
    INSERT OR REPLACE INTO canonical_entities(
        name,
        entity_type,
        frequency,
        confidence,
        evidence_count
    )
    VALUES(?,?,?,?,?)
    """, (
        name,
        etype,
        freq,
        conf,
        freq
    ))

conn.commit()

# --------------------------------------------------
# REPORTS
# --------------------------------------------------

output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

for category in [
    "PERSON",
    "COMPANY",
    "PROJECT",
    "TECHNOLOGY",
    "SKILL",
    "OTHER"
]:

    cur.execute("""
    SELECT
        name,
        frequency
    FROM canonical_entities
    WHERE entity_type=?
    ORDER BY frequency DESC
    LIMIT 100
    """, (category,))

    data = [
        dict(r)
        for r in cur.fetchall()
    ]

    with open(
        output_dir /
        f"{category.lower()}.json",
        "w"
    ) as f:
        json.dump(
            data,
            f,
            indent=2
        )

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print("\n" + "="*60)
print("SEMANTIC AUDIT COMPLETE")
print("="*60)

for k,v in sorted(stats.items()):
    print(f"{k:<15} {v}")

print("\nTOP PROJECTS\n")

cur.execute("""
SELECT
    name,
    frequency
FROM canonical_entities
WHERE entity_type='PROJECT'
ORDER BY frequency DESC
LIMIT 20
""")

for row in cur.fetchall():
    print(
        row["frequency"],
        row["name"]
    )

print("\nTOP COMPANIES\n")

cur.execute("""
SELECT
    name,
    frequency
FROM canonical_entities
WHERE entity_type='COMPANY'
ORDER BY frequency DESC
LIMIT 20
""")

for row in cur.fetchall():
    print(
        row["frequency"],
        row["name"]
    )

conn.close()
