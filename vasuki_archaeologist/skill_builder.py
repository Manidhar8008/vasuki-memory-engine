import sqlite3

DB="/data/data/com.termux/files/home/vasuki/vasuki.db"

SKILLS = [
    "python",
    "sqlite",
    "fastapi",
    "termux",
    "git",
    "github",
    "agent",
    "rag",
    "embedding",
    "prompt",
    "llm"
]

conn = sqlite3.connect(DB)
cur = conn.cursor()

for skill in SKILLS:

    cur.execute("""
    SELECT COUNT(*)
    FROM documents
    WHERE lower(content) LIKE ?
    """,
    (f"%{skill}%",))

    count = cur.fetchone()[0]

    if count > 0:

        cur.execute("""
        INSERT INTO skills(
            skill_name,
            confidence,
            evidence_count
        )
        VALUES(?,?,?)
        """,
        (
            skill,
            min(count/10,1.0),
            count
        ))

conn.commit()
conn.close()

print("SKILLS BUILT")
