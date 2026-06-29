import sqlite3
from collections import Counter

db = sqlite3.connect("vasuki.db")
cur = db.cursor()

print("\n=== FOUNDER REASONER ===\n")

categories = [
    "GOAL",
    "PROJECT",
    "DECISION",
    "FAILURE",
    "LEARNING"
]

for cat in categories:

    rows = cur.execute("""
    SELECT description
    FROM ontology_objects
    WHERE object_type = ?
    LIMIT 100
    """,(cat,)).fetchall()

    print(f"\n{cat}")
    print("="*60)

    for r in rows[:10]:
        print("-",r[0][:150])
