import sqlite3

conn=sqlite3.connect("founder.db")
cur=conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS founder_emotions(

id INTEGER PRIMARY KEY,

source TEXT,

emotion TEXT,

intensity INTEGER,

evidence TEXT,

created_at TEXT DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()
conn.close()

print("EMOTION TABLE READY")
