#!/usr/bin/env python3

import sqlite3
from pathlib import Path

DB = str(Path.home() / "vasuki" / "vasuki.db")

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("DELETE FROM knowledge_assets")

# -----------------------------
# scoring helpers
# -----------------------------

PROJECT_WORDS = [
    "product",
    "architecture",
    "agent",
    "system",
    "platform",
    "workflow",
    "roadmap",
    "prototype",
    "startup",
    "business requirements"
]

BUSINESS_WORDS = [
    "revenue",
    "pricing",
    "customer",
    "market",
    "sales",
    "startup",
    "business",
    "monetization"
]

LEARNING_WORDS = [
    "research",
    "analysis",
    "study",
    "guide",
    "tutorial",
    "learning",
    "course"
]

FOUNDER_WORDS = [
    "manidhar",
    "janani",
    "found the unfindable",
    "personal",
    "second brain",
    "life operating system"
]

def score(text, words):
    text = text.lower()
    total = 0

    for w in words:
        if w in text:
            total += 1

    return min(100, total * 15)

# -----------------------------
# documents
# -----------------------------

cur.execute("""
SELECT id,title,content
FROM documents
""")

docs = cur.fetchall()

for row in docs:

    doc_id = row["id"]
    title = row["title"] or ""
    content = row["content"] or ""

    text = (title + "\n" + content[:15000]).lower()

    founder = score(text, FOUNDER_WORDS)
    project = score(text, PROJECT_WORDS)
    business = score(text, BUSINESS_WORDS)
    learning = score(text, LEARNING_WORDS)

    # category

    category = "GENERAL"

    if founder >= 45 and project >= 45:
        category = "PRODUCT"

    elif learning >= 45:
        category = "RESEARCH"

    elif business >= 45:
        category = "BUSINESS"

    elif "resume" in text or "offer" in text:
        category = "CAREER"

    elif "statement" in text:
        category = "FINANCE"

    elif "act" in text or "legal" in text:
        category = "LEGAL"

    importance = round(
        (0.35 * founder)
        + (0.30 * project)
        + (0.20 * business)
        + (0.15 * learning),
        2
    )

    summary = content[:500].replace("\n", " ")

    confidence = round(
        min(100, importance + 10),
        2
    )

    cur.execute("""
    INSERT INTO knowledge_assets(
        document_id,
        title,
        category,
        founder_score,
        project_score,
        business_score,
        learning_score,
        confidence,
        summary,
        importance_score
    )
    VALUES(?,?,?,?,?,?,?,?,?,?)
    """, (
        doc_id,
        title,
        category,
        founder,
        project,
        business,
        learning,
        confidence,
        summary,
        importance
    ))

conn.commit()

cur.execute("""
SELECT COUNT(*)
FROM knowledge_assets
""")

print("Knowledge Assets:", cur.fetchone()[0])

conn.close()
