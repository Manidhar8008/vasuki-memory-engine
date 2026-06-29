import sqlite3

conn=sqlite3.connect("vasuki.db")
cur=conn.cursor()

types = [
    "PROJECT",
    "GOAL",
    "DECISION",
    "FAILURE",
    "LEARNING"
]

print("\n=== FOUNDER STATE ===\n")

for t in types:

    cur.execute("""
    SELECT COUNT(*)
    FROM ontology_objects
    WHERE object_type=?
    """,(t,))

    n = cur.fetchone()[0]

    print(f"{t:<12} {n}")
