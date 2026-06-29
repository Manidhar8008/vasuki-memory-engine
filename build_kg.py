import sqlite3

conn=sqlite3.connect("vasuki.db")
cur=conn.cursor()

cur.execute("DELETE FROM kg_nodes")
cur.execute("DELETE FROM kg_edges")

PROJECTS=[
"vasuki",
"janani",
"mw.ai",
"aim1000"
]

for p in PROJECTS:

    cur.execute("""
    INSERT INTO kg_nodes(
    node_type,
    node_name
    )
    VALUES(
    'project',
    ?
    )
    """,(p,))

cur.execute("""
SELECT entity
FROM entities
LIMIT 5000
""")

for row in cur.fetchall():

    entity=row[0]

    cur.execute("""
    INSERT INTO kg_nodes(
    node_type,
    node_name
    )
    VALUES(
    'entity',
    ?
    )
    """,(entity,))

conn.commit()

print("GRAPH BUILT")

conn.close()
