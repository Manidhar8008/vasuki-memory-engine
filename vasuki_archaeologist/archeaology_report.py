import sqlite3

conn = sqlite3.connect(
    "vasuki.db"
)

cur = conn.cursor()

print("\n=== FILES ===")

try:
    cur.execute(
        "SELECT COUNT(*) FROM files"
    )
    print(cur.fetchone()[0])
except:
    pass

print("\n=== MEMORIES ===")

try:
    cur.execute(
        "SELECT COUNT(*) FROM memories"
    )
    print(cur.fetchone()[0])
except:
    pass

print("\n=== EVENTS ===")

try:
    cur.execute(
        "SELECT COUNT(*) FROM events"
    )
    print(cur.fetchone()[0])
except:
    pass

conn.close()
