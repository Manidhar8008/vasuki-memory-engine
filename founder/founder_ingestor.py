import sqlite3
import os

DB="founder.db"

conn=sqlite3.connect(DB)

cur=conn.cursor()

with open("sample_files.txt") as f:

    files=f.readlines()

for file in files:

    file=file.strip()

    if not os.path.exists(file):

        continue

    name=os.path.basename(file)

    ext=os.path.splitext(file)[1]

    size=os.path.getsize(file)

    cur.execute("""

    INSERT INTO founder_artifacts(

    path,
    filename,
    filetype,
    size

    )

    VALUES(?,?,?,?)

    """,(

    file,
    name,
    ext,
    size

    ))

conn.commit()

conn.close()

print("DONE")
