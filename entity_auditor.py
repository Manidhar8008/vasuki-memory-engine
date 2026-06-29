import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

rows = cur.execute("""
SELECT entity
FROM entities
""").fetchall()

good = 0
bad = 0

for row in rows:

    e = row[0] or ""

    if len(e) < 3:
        bad += 1

    elif any(ch.isdigit() for ch in e):
        bad += 1

    elif "." in e:
        bad += 1

    else:
        good += 1

print("\nENTITY QUALITY REPORT\n")

print("GOOD:", good)
print("BAD :", bad)

conn.close()
