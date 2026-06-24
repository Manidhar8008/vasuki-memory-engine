import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS projects(
 id INTEGER PRIMARY KEY,
 name TEXT,
 description TEXT,
 status TEXT,
 created_at TEXT
)
""")

KEYWORDS = [
"vasuki",
"janani",
"mw.ai",
"aim1000",
"portfolio",
"founder corpus"
]

cur.execute("""
SELECT content
FROM documents
""")

for row in cur.fetchall():

    text = row[0] or ""

    lower = text.lower()

    for keyword in KEYWORDS:

        if keyword in lower:

            cur.execute("""
            INSERT INTO projects(
            name,
            description,
            status
            )
            VALUES(?,?,?)
            """,(keyword,text[:500],"active"))

conn.commit()

print("PROJECTS BUILT")

conn.close()
