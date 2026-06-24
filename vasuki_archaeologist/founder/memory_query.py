import sqlite3

conn=sqlite3.connect("founder.db")
cur=conn.cursor()

cur.execute("""
SELECT title,
word_count
FROM founder_memory
""")

for row in cur.fetchall():

    print(row)

conn.close()
