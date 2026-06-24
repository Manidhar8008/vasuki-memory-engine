import sqlite3

DB="founder.db"

conn=sqlite3.connect(DB)
cur=conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS founder_memory(

id INTEGER PRIMARY KEY,

title TEXT,

content TEXT,

word_count INTEGER,

created_at TEXT DEFAULT CURRENT_TIMESTAMP

)
""")

with open(
    "birthday_memory.md",
    "r",
    encoding="utf-8"
) as f:

    content=f.read()

cur.execute("""
INSERT INTO founder_memory(

title,
content,
word_count

)

VALUES(?,?,?)
""",
(
    "Birthday Memory Injection",
    content,
    len(content.split())
))

conn.commit()
conn.close()

print("MEMORY INJECTED")
