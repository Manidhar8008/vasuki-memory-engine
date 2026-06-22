import sqlite3
import os

DB="founder.db"

conn=sqlite3.connect(DB)
cur=conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS founder_content(
id INTEGER PRIMARY KEY,
filename TEXT,
content TEXT
)
""")

FILES=[
"roadmap.md",
"Multi-Model Personalized AI Agent Architecture (Research Analysis).txt",
"memory_builder.py",
"memory_graph.py",
"vasuki.py"
]

for file in FILES:

    if os.path.exists(file):

        with open(file,"r",errors="ignore") as f:

            text=f.read()

        cur.execute("""
        INSERT INTO founder_content(
        filename,
        content
        )
        VALUES(?,?)
        """,
        (
        file,
        text
        ))

conn.commit()
conn.close()

print("DONE")
