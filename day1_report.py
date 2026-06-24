import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

print("\n=== VASUKI DAY 1 REPORT ===\n")

tables = [
    "memories",
    "entities",
    "ontology_objects",
    "founder_truths"
]

for table in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        print(f"{table:<20} {count}")
    except:
        print(f"{table:<20} ERROR")

print("\n=== TRUTHS ===\n")

for t in ["PROJECT","GOAL","DECISION","FAILURE","LEARNING"]:

    print(f"\n{t}")
    print("-"*40)

    cur.execute("""
    SELECT truth
    FROM founder_truths
    WHERE truth_type=?
    LIMIT 10
    """,(t,))

    rows = cur.fetchall()

    for r in rows:
        print("-", r[0])

conn.close()
