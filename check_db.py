import sqlite3

conn = sqlite3.connect("vasuki.db")

cur = conn.cursor()

count = cur.execute(
    "SELECT COUNT(*) FROM documents"
).fetchone()[0]

print("DOCUMENTS:", count)

conn.close()
