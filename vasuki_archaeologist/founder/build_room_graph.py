import sqlite3

conn=sqlite3.connect("founder.db")
cur=conn.cursor()

links=[

("MANIDHAR","CREATED","VASUKI",100),

("MANIDHAR","FOUNDED","MW.AI",100),

("MANIDHAR","CREATED","JANANI",95),

("ONEPLUS","STREAMS_TO","VASUKI",90),

("REALME","STREAMS_TO","VASUKI",80),

("LAPTOP","STREAMS_TO","VASUKI",100),

("VASUKI","SUPPORTS","MW.AI",95),

("VASUKI","SUPPORTS","JANANI",95),

("VASUKI","USES","SQLITE",90),

("VASUKI","USES","PYTHON",90),

("VASUKI","USES","TERMUX",90),

("VASUKI","USES","GITHUB",85),

("VASUKI","USES","TELEGRAM",80)

]

for link in links:

    cur.execute("""

    INSERT INTO identity_relationships(

    source_entity,
    relationship,
    target_entity,
    weight

    )

    VALUES(?,?,?,?)

    """,link)

conn.commit()

conn.close()

print("ROOM GRAPH BUILT")
