import sqlite3
import sys

query=" ".join(sys.argv[1:])

conn=sqlite3.connect("vasuki.db")
cur=conn.cursor()

rows=cur.execute("""
SELECT title,
substr(content,1,500)
FROM founder_notes
WHERE lower(content)
LIKE lower(?)
LIMIT 20
""",(f"%{query}%",)).fetchall()

for title,text in rows:

    print("\n")
    print("="*80)
    print(title)
    print("="*80)
    print(text)

conn.close()
