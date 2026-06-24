import sqlite3

conn=sqlite3.connect("vasuki.db")
cur=conn.cursor()

tables=[
"documents",
"memories",
"entities",
"goals",
"projects",
"decisions",
"failures",
"learnings"
]

print("\n=== VASUKI FOUNDER DASHBOARD ===\n")

for t in tables:
    try:
        count=cur.execute(
        f"SELECT COUNT(*) FROM {t}"
        ).fetchone()[0]

        print(f"{t:<15} {count}")

    except:
        pass
