import sqlite3

DB = "vasuki.db"

AI = [
    "agent","agents","llm","rag","retrieval",
    "memory","embedding","vector","prompt",
    "automation","workflow","model"
]

FINANCE = [
    "accounting","audit","tax","gst",
    "financial","bank","balance",
    "investment","budget","cost"
]

CAREER = [
    "resume","cv","offer","interview",
    "employment","job","career"
]

PSYCHOLOGY = [
    "psychology","cognitive",
    "behavior","emotion","personality"
]

LEGAL = [
    "court","law","legal",
    "offence","act","section"
]

conn = sqlite3.connect(DB)
cur = conn.cursor()

rows = cur.execute(
    "SELECT id,title,content FROM documents"
).fetchall()

for doc_id,title,content in rows:

    text = str(content).lower()

    category = "UNKNOWN"

    if any(word in text for word in AI):
        category = "AI"

    elif any(word in text for word in FINANCE):
        category = "FINANCE"

    elif any(word in text for word in CAREER):
        category = "CAREER"

    elif any(word in text for word in PSYCHOLOGY):
        category = "PSYCHOLOGY"

    elif any(word in text for word in LEGAL):
        category = "LEGAL"

    cur.execute(
        "UPDATE documents SET category=? WHERE id=?",
        (category, doc_id)
    )

conn.commit()
conn.close()

print("Classification complete.")
