import sqlite3

conn=sqlite3.connect("founder.db")
cur=conn.cursor()

cur.execute("""

CREATE TABLE IF NOT EXISTS architect_tasks(

id INTEGER PRIMARY KEY,

project TEXT,

task TEXT,

priority INTEGER,

status TEXT

)

""")

tasks=[

("vasuki","voice interface",1,"todo"),

("vasuki","memory graph",1,"todo"),

("vasuki","agent runtime",1,"todo"),

("vasuki","telegram connector",2,"todo"),

("mw.ai","crm engine",2,"todo"),

("janani","personal intelligence layer",2,"todo")

]

for t in tasks:

    cur.execute("""

    INSERT INTO architect_tasks(

    project,
    task,
    priority,
    status

    )

    VALUES(?,?,?,?)

    """,t)

conn.commit()
conn.close()

print("ARCHITECT READY")
