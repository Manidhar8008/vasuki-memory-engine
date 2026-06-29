import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

query = input("Search: ")

rows = cur.execute(
    """
    SELECT title, chars
    FROM documents
    WHERE content LIKE ?
    """,
    (f"%{query}%",)
).fetchall()

for row in rows:
    print("\nFound:")
    print(row)

conn.close()
