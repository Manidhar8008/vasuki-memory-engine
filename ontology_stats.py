import sqlite3

conn=sqlite3.connect("vasuki.db")
cur=conn.cursor()

print("\n=== ONTOLOGY ===\n")

cur.execute("""
SELECT object_type,COUNT(*)
FROM ontology_objects
GROUP BY object_type
ORDER BY COUNT(*) DESC
""")

for row in cur.fetchall():
    print(row)
