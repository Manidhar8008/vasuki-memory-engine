import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

tables = [
    "documents",
    "memories",
    "entities",
    "goals",
    "decisions",
    "learnings",
    "failures"
]

print("\n=== VASUKI INTELLIGENCE DASHBOARD ===\n")

for table in tables:

    try:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        print(f"{table:<15} {count}")

    except:
        pass

conn.close()
