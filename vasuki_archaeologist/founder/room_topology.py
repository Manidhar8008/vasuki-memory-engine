import sqlite3

conn=sqlite3.connect("founder.db")
cur=conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS room_topology(

id INTEGER PRIMARY KEY,

source TEXT,

target TEXT,

relationship TEXT

)
""")

links=[

("oneplus","vasuki","STREAMS_TO"),

("realme","vasuki","STREAMS_TO"),

("laptop","vasuki","STREAMS_TO"),

("manidhar","vasuki","OPERATES"),

("vasuki","mw.ai","SUPPORTS"),

("vasuki","janani","SUPPORTS")

]

for l in links:

    cur.execute("""
    INSERT INTO room_topology(
    source,
    target,
    relationship
    )
    VALUES(?,?,?)
    """,l)

conn.commit()
conn.close()

print("ROOM TOPOLOGY READY")
