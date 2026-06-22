import sqlite3

conn=sqlite3.connect("founder.db")
cur=conn.cursor()

cur.execute("""

CREATE TABLE IF NOT EXISTS vision(

id INTEGER PRIMARY KEY,

entity TEXT,

vision TEXT,

target_year TEXT,

status TEXT

)

""")

conn.commit()
conn.close()

print("VISION READY")
