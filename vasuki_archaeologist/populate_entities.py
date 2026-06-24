	mport sqlite3
import re

DB = "/data/data/com.termux/files/home/vasuki/vasuki.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
SELECT id, content
FROM documents
""")

docs = cur.fetchall()

for doc_id, content in docs:

if not content:
    continue

entities = set()

# Capitalized words
matches = re.findall(
    r'\b[A-Z][A-Za-z0-9._-]{2,}\b',
    content
)

for m in matches:
    entities.add(m.strip())

# Known Vasuki concepts
text = content.lower()

known = [
    "vasuki",
    "mw.ai",
    "janani",
    "termux",
    "sqlite",
    "fastapi",
    "ollama",
    "warangal",
    "crm"
]

for k in known:
    if k in text:
        entities.add(k)

for entity in entities:

    cur.execute("""
    INSERT OR IGNORE INTO entities(
        entity,
        entity_type
    )
    VALUES (?,?)
    """,
    (
        entity,
        "concept"
    ))

    cur.execute("""
    SELECT id
    FROM entities
    WHERE entity=?
    """,
    (entity,))

    row = cur.fetchone()

    if not row:
        continue

    entity_id = row[0]

    cur.execute("""
    INSERT INTO entity_mentions(
        artifact_id,
        entity_id,
        count
    )
    VALUES (?,?,?)
    """,
    (
        doc_id,
        entity_id,
        1
    ))

conn.commit()
conn.close()

print("Entities Loaded")
