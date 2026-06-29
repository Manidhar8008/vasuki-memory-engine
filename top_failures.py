import sqlite3

conn=sqlite3.connect("vasuki.db")
cur=conn.cursor()

cur.execute("""
SELECT description
FROM ontology_objects
WHERE object_type='FAILURE'
LIMIT 30
""")

for row in cur.fetchall():
    print("\n",row[0][:300])
