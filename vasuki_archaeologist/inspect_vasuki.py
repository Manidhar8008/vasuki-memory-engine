import sqlite3

DB = "/data/data/com.termux/files/home/vasuki/vasuki.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

tables = [
    "files",
    "documents",
    "memories",
    "entities",
    "entity_mentions",
    "entity_relationships",
    "relationships",
    "timeline",
    "skills",
    "events",
    "evidence"
]

print("\nVASUKI DATABASE PROFILE\n")

for table in tables:

    try:

        cur.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        count = cur.fetchone()[0]

        print(
            f"{table:<25} {count}"
        )

    except Exception as e:

        print(
            f"{table:<25} ERROR"
        )

conn.close()
