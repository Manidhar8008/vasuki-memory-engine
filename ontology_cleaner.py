import sqlite3
import re

DB = "vasuki.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

# Add columns if missing
try:
    cur.execute("""
    ALTER TABLE ontology_objects
    ADD COLUMN quality_score REAL DEFAULT 5
    """)
except:
    pass

try:
    cur.execute("""
    ALTER TABLE ontology_objects
    ADD COLUMN quality_reason TEXT
    """)
except:
    pass

cur.execute("""
SELECT id,name,description
FROM ontology_objects
""")

rows = cur.fetchall()

updated = 0

for oid,name,desc in rows:

    text = f"{name or ''} {desc or ''}".lower()

    score = 5
    reason = []

    # Too long
    if len(name or "") > 80:
        score -= 3
        reason.append("long_name")

    # Giant paragraphs
    if len(text) > 300:
        score -= 2
        reason.append("paragraph")

    # Bullets
    if "-" in text[:10]:
        score -= 2
        reason.append("bullet")

    # URLs
    if "http" in text:
        score -= 2
        reason.append("url")

    # Too many numbers
    digits = len(re.findall(r"\d", text))
    if digits > 15:
        score -= 2
        reason.append("numeric_noise")

    # Action/task style
    action_words = [
        "launch",
        "create",
        "build",
        "write",
        "track",
        "offer",
        "post",
        "start"
    ]

    if any(word in text for word in action_words):
        score -= 1
        reason.append("task")

    # Strong founder concepts
    founder_words = [
        "vasuki",
        "janani",
        "founder",
        "startup",
        "architecture",
        "remote",
        "ai",
        "memory",
        "ontology"
    ]

    if any(word in text for word in founder_words):
        score += 2
        reason.append("founder_signal")

    score = max(0,min(score,10))

    cur.execute("""
    UPDATE ontology_objects
    SET quality_score=?,
        quality_reason=?
    WHERE id=?
    """,(score,",".join(reason),oid))

    updated += 1

conn.commit()

print("="*50)
print("ONTOLOGY CLEAN COMPLETE")
print("="*50)
print("UPDATED:",updated)

cur.execute("""
SELECT quality_score,COUNT(*)
FROM ontology_objects
GROUP BY quality_score
ORDER BY quality_score DESC
""")

for row in cur.fetchall():
    print(row)

conn.close()
