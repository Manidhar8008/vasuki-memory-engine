import sqlite3
from pathlib import Path

DB="vasuki.db"

conn=sqlite3.connect(DB)
cur=conn.cursor()

root="/storage/emulated/0"

count=0

for file in Path(root).rglob("*.md"):

    try:

        text=file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        cur.execute("""
        INSERT INTO founder_notes(
            path,
            title,
            content,
            chars,
            category
        )
        VALUES(?,?,?,?,?)
        """,(
            str(file),
            file.name,
            text,
            len(text),
            "markdown"
        ))

        count+=1

        print("[MD]",count,file.name)

    except:
        pass

conn.commit()
conn.close()

print("\nDONE:",count)
