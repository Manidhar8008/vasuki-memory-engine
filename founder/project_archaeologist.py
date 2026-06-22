import sqlite3
import re

DB = "founder.db"

PROJECTS = [
    "vasuki",
    "mw.ai",
    "janani"
]

conn = sqlite3.connect(DB)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS project_evidence(
id INTEGER PRIMARY KEY,
project TEXT,
filename TEXT,
mentions INTEGER
)
""")

cur.execute("""
SELECT filename,content
FROM founder_core_files
""")

rows = cur.fetchall()

for filename,content in rows:

    text = content.lower()

    for project in PROJECTS:

        count = text.count(project)

        if count > 0:

            cur.execute("""
            INSERT INTO project_evidence(
            project,
            filename,
            mentions
            )
            VALUES(?,?,?)
            """,
            (
                project,
                filename,
                count
            ))

conn.commit()

conn.close()

print("PROJECT EVIDENCE BUILT")
