import sqlite3

conn = sqlite3.connect("founder.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS founder_entities(

id INTEGER PRIMARY KEY,

name TEXT UNIQUE,

entity_type TEXT,

importance INTEGER,

description TEXT

)
""")

entities = [

("MANIDHAR","FOUNDER",100,"Creator of Vasuki"),

("VASUKI","ROOM_OS",100,"Persistent intelligence system"),

("MW.AI","COMPANY",95,"Business intelligence company"),

("JANANI","PROJECT",90,"Personal intelligence layer"),

("GITHUB","PLATFORM",80,"Code repository"),

("TELEGRAM","PLATFORM",75,"Communication layer"),

("SQLITE","TECHNOLOGY",85,"Memory database"),

("PYTHON","TECHNOLOGY",90,"Primary language"),

("TERMUX","DEVICE_RUNTIME",90,"Mobile development environment"),

("FASTAPI","TECHNOLOGY",70,"Backend framework")

]

for entity in entities:

    cur.execute("""

    INSERT OR IGNORE INTO founder_entities(

    name,
    entity_type,
    importance,
    description

    )

    VALUES(?,?,?,?)

    """,entity)

conn.commit()

cur.execute("""
SELECT
name,
entity_type,
importance
FROM founder_entities
ORDER BY importance DESC
""")

rows = cur.fetchall()

print("\nFOUNDER ENTITIES\n")

for row in rows:

    print(row)

conn.close()
