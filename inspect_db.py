import sqlite3

db = sqlite3.connect("vasuki.db")
cur = db.cursor()

tables = [
    "founder_artifacts",
    "founder_evidence",
    "founder_insights",
    "founder_patterns",
    "founder_world_model"
]

for t in tables:

    print("\n====", t, "====")

    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        print("Rows:", cur.fetchone()[0])

        cur.execute(f"SELECT * FROM {t} LIMIT 3")

        for row in cur.fetchall():
            print(row)

    except Exception as e:
        print("ERROR:", e)
