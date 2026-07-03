#!/usr/bin/env python3

import sqlite3
from pathlib import Path

DB = str(Path.home() / "vasuki" / "vasuki.db")

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# -------------------------------------------------
# RESET FACTS
# -------------------------------------------------

cur.execute("DELETE FROM facts")

# -------------------------------------------------
# KNOWN PROJECTS
# -------------------------------------------------

PROJECTS = [
    "Vasuki",
    "Janani",
    "MW.AI",
    "Found the Unfindable",
    "Lime IoT ML Platform",
    "AI-powered Supply Chain Automation System"
]

COMPANIES = [
    "Cognizant",
    "Genpact",
    "Lime",
    "OpenAI",
    "Google",
    "Microsoft"
]

TECH = [
    "Python",
    "FastAPI",
    "SQLite",
    "PostgreSQL",
    "React",
    "TypeScript",
    "Docker",
    "GitHub",
    "Qdrant",
    "Ollama"
]

# -------------------------------------------------
# INSERT FACT
# -------------------------------------------------

def add_fact(subject, predicate, obj, evidence, confidence):

    cur.execute("""
    INSERT OR IGNORE INTO facts(
        subject,
        predicate,
        object,
        evidence,
        confidence
    )
    VALUES(?,?,?,?,?)
    """, (
        subject,
        predicate,
        obj,
        evidence[:1000],
        confidence
    ))

# -------------------------------------------------
# DOCUMENTS
# -------------------------------------------------

print("Scanning documents...")

cur.execute("""
SELECT title, content
FROM documents
""")

for row in cur.fetchall():

    title = str(row["title"] or "")
    content = str(row["content"] or "")

    text = (title + "\n" + content[:10000]).lower()

    for project in PROJECTS:
        if project.lower() in text:
            add_fact(
                "Manidhar",
                "BUILT",
                project,
                title,
                0.90
            )

    for company in COMPANIES:
        if company.lower() in text:
            add_fact(
                "Manidhar",
                "ASSOCIATED_WITH",
                company,
                title,
                0.80
            )

    for tech in TECH:
        if tech.lower() in text:
            add_fact(
                "Manidhar",
                "USES",
                tech,
                title,
                0.75
            )

# -------------------------------------------------
# MEMORIES
# -------------------------------------------------

print("Scanning memories...")

cur.execute("""
SELECT memory
FROM memories
""")

for row in cur.fetchall():

    memory = str(row["memory"] or "").lower()

    for tech in TECH:

        if tech.lower() in memory:

            add_fact(
                "Manidhar",
                "KNOWS",
                tech,
                memory,
                0.70
            )

# -------------------------------------------------
# OCR
# -------------------------------------------------

print("Scanning OCR...")

try:

    cur.execute("""
    SELECT raw_text
    FROM ocr_records
    """)

    for row in cur.fetchall():

        txt = str(row["raw_text"] or "").lower()

        for company in COMPANIES:

            if company.lower() in txt:

                add_fact(
                    "Manidhar",
                    "MENTIONS",
                    company,
                    txt[:500],
                    0.60
                )

except Exception as e:
    print(e)

conn.commit()

# -------------------------------------------------
# REPORT
# -------------------------------------------------

cur.execute("""
SELECT COUNT(*)
FROM facts
""")

count = cur.fetchone()[0]

print("\n========================")
print("FACT EXTRACTION COMPLETE")
print("========================")
print("TOTAL FACTS:", count)

cur.execute("""
SELECT predicate,
       COUNT(*) c
FROM facts
GROUP BY predicate
ORDER BY c DESC
""")

print("\nFACT BREAKDOWN\n")

for row in cur.fetchall():
    print(
        row["predicate"],
        row["c"]
    )

conn.close()

