import sqlite3

conn=sqlite3.connect("vasuki.db")
cur=conn.cursor()

tests = []

cur.execute("""
SELECT COUNT(*)
FROM ontology_objects
""")

tests.append(
    ("ontology rows",
     cur.fetchone()[0] > 0)
)

cur.execute("""
SELECT COUNT(*)
FROM ontology_objects
WHERE object_type='PROJECT'
""")

tests.append(
    ("projects exist",
     cur.fetchone()[0] > 0)
)

cur.execute("""
SELECT COUNT(*)
FROM ontology_objects
WHERE object_type='GOAL'
""")

tests.append(
    ("goals exist",
     cur.fetchone()[0] > 0)
)

print("\n=== TESTS ===\n")

for name,result in tests:

    if result:
        print("[PASS]",name)
    else:
        print("[FAIL]",name)
