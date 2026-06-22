import sqlite3

conn = sqlite3.connect(
    "vasuki.db"
)

cur = conn.cursor()

cur.execute("""
SELECT content
FROM documents
""")

for row in cur.fetchall():

    text = row[0]

    if "vasuki" in text.lower():

        if "memory" in text.lower():

            print(
                "VASUKI -> MEMORY"
            )

        if "janani" in text.lower():

            print(
                "VASUKI -> JANANI"
            )

        if "agent" in text.lower():

            print(
                "VASUKI -> AGENT"
            )

conn.close()
