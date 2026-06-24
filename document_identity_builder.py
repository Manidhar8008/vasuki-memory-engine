import sqlite3
import re

DB = "vasuki.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS document_identity (
    id INTEGER PRIMARY KEY,
    document_id INTEGER,
    path TEXT,
    title TEXT,
    document_type TEXT,
    project TEXT,
    importance INTEGER,
    summary TEXT,
    suggested_name TEXT
)
""")

docs = cur.execute("""
SELECT id,title,path,content
FROM documents
LIMIT 100
""").fetchall()


def classify(title, content):

    text = (title + " " + (content[:3000] if content else "")).lower()

    if any(x in text for x in [
        "payslip",
        "salary",
        "form16",
        "offer letter",
        "appointment"
    ]):
        return "career_document", "career", 9

    if any(x in text for x in [
        "invoice",
        "payment",
        "receipt"
    ]):
        return "financial_document", "finance", 7

    if any(x in text for x in [
        "agent",
        "fastapi",
        "python",
        "rag",
        "llm",
        "embedding"
    ]):
        return "ai_research", "vasuki", 10

    if any(x in text for x in [
        "novel",
        "story",
        "found the unfindable"
    ]):
        return "creative_work", "ani.ai", 8

    return "unknown", "unclassified", 3


for doc_id, title, path, content in docs:

    dtype, project, importance = classify(
        title,
        content or ""
    )

    summary = (
        (content or "")
        .replace("\n", " ")
        [:300]
    )

    clean_title = re.sub(
        r'[^a-zA-Z0-9_ ]',
        '',
        title
    )

    suggested_name = (
        f"{project}_{dtype}_{doc_id}.pdf"
    )

    cur.execute("""
    INSERT INTO document_identity (
        document_id,
        path,
        title,
        document_type,
        project,
        importance,
        summary,
        suggested_name
    )
    VALUES (?,?,?,?,?,?,?,?)
    """, (
        doc_id,
        path,
        title,
        dtype,
        project,
        importance,
        summary,
        suggested_name
    ))

conn.commit()

count = cur.execute(
    "SELECT COUNT(*) FROM document_identity"
).fetchone()[0]

print(f"\nProcessed: {count}")

conn.close()
