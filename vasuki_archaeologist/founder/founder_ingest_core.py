import sqlite3
import os

DB = "founder.db"

CORE = "./founder_core"

conn = sqlite3.connect(DB)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS founder_core_files(
id INTEGER PRIMARY KEY,
filename TEXT,
content TEXT
)
""")

for file in os.listdir(CORE):

    path = os.path.join(CORE,file)

    try:

        with open(path,"r",encoding="utf-8",errors="ignore") as f:

            content = f.read()

        cur.execute("""
        INSERT INTO founder_core_files(
        filename,
        content
        )
        VALUES(?,?)
        """,(file,content))

    except:
        pass

conn.commit()

conn.close()

print("CORE INGESTED")
