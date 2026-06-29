import sqlite3
import re

DB="vasuki.db"

conn=sqlite3.connect(DB)
cur=conn.cursor()

rows=cur.execute("""
SELECT file_path, raw_text
FROM ocr_records
WHERE LENGTH(raw_text) > 500
LIMIT 1000
""").fetchall()

for path,text in rows:

    text_low=text.lower()

    evidence=[]

    if "github" in text_low:
        evidence.append("github_activity")

    if "fastapi" in text_low:
        evidence.append("fastapi_activity")

    if "ollama" in text_low:
        evidence.append("ollama_activity")

    if "resume" in text_low:
        evidence.append("resume_activity")

    if "job" in text_low:
        evidence.append("job_search")

    if "applied" in text_low:
        evidence.append("job_application")

    if "intern" in text_low:
        evidence.append("intern_management")

    if "client" in text_low:
        evidence.append("client_work")

    if "vasuki" in text_low:
        evidence.append("vasuki_project")

    if "mw.ai" in text_low or "mw ai" in text_low:
        evidence.append("mw_project")

    for e in evidence:

        cur.execute("""
        INSERT INTO evidence(
            source_type,
            source_path,
            evidence_type,
            evidence_text,
            confidence
        )
        VALUES(?,?,?,?,?)
        """,(
            "ocr",
            path,
            e,
            text[:500],
            0.80
        ))

conn.commit()
conn.close()

print("Evidence built.")
