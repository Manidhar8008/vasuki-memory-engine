import sqlite3

conn=sqlite3.connect("founder.db")
cur=conn.cursor()

cur.execute("""

CREATE TABLE IF NOT EXISTS room_entities(

id INTEGER PRIMARY KEY,

room_name TEXT,

entity_type TEXT,

entity_name TEXT,

status TEXT

)

""")

conn.commit()
conn.close()

print("ROOM AGENT READY")
