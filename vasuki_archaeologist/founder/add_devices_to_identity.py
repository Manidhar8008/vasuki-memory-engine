import sqlite3

conn = sqlite3.connect("founder.db")
cur = conn.cursor()

devices = [

("ONEPLUS","DEVICE",95,"Primary capture device"),

("LAPTOP","DEVICE",95,"Primary compute device"),

("REALME","DEVICE",85,"Field device")

]

for d in devices:

    cur.execute("""

    INSERT OR IGNORE INTO founder_entities(

    name,
    entity_type,
    importance,
    description

    )

    VALUES(?,?,?,?)

    """,d)

conn.commit()

conn.close()

print("DEVICES ADDED")
