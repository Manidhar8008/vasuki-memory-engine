import sqlite3

conn=sqlite3.connect("founder.db")
cur=conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS devices(

id INTEGER PRIMARY KEY,

device_name TEXT,

device_type TEXT,

role TEXT,

status TEXT

)
""")

devices=[

("oneplus","phone","capture","active"),

("realme","phone","field","active"),

("laptop","computer","compute","active")

]

for d in devices:

    cur.execute("""
    INSERT INTO devices(
    device_name,
    device_type,
    role,
    status
    )
    VALUES(?,?,?,?)
    """,d)

conn.commit()
conn.close()

print("DEVICES REGISTERED")
