import sqlite3

conn=sqlite3.connect("vasuki.db")
cur=conn.cursor()

for t in [
    "PROJECT",
    "GOAL",
    "DECISION",
    "FAILURE",
    "LEARNING"
]:

    print("\n")
    print("="*80)
    print(t)
    print("="*80)

    cur.execute("""
    SELECT description
    FROM ontology_objects
    WHERE object_type=?
    LIMIT 10
    """,(t,))

    for row in cur.fetchall():
        print("-",row[0][:200])
