import sqlite3

DB="vasuki.db"

KEYWORDS = {
    "github":"development",
    "fastapi":"development",
    "python":"development",
    "ollama":"ai",
    "openai":"ai",
    "gemini":"ai",
    "llm":"ai",
    "resume":"career",
    "interview":"career",
    "job":"career",
    "client":"business",
    "intern":"business",
    "startup":"founder",
    "founder":"founder",
    "vasuki":"vasuki",
    "mw.ai":"mwai",
    "janani":"janani"
}

conn=sqlite3.connect(DB)
cur=conn.cursor()

rows=cur.execute("""
SELECT file_path,raw_text
FROM ocr_records
WHERE LENGTH(raw_text)>500
""").fetchall()

count=0

for path,text in rows:

    if not text:
        continue

    t=text.lower()

    for keyword,etype in KEYWORDS.items():

        if keyword in t:

            cur.execute("""
            INSERT INTO founder_evidence(
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
                etype,
                keyword,
                0.8
            ))

            count+=1

conn.commit()

print()
print("="*60)
print("FOUNDER EVIDENCE CREATED")
print("="*60)
print("TOTAL:",count)

conn.close()
