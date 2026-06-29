import sqlite3

DB = "vasuki.db"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

print("\n=== ASK VASUKI ===\n")

while True:

    question = input("Ask> ")

    if question.lower() in ["exit", "quit"]:
        break

    if "project" in question.lower():

        try:
            cursor.execute("""
                SELECT project,
                       COUNT(*)
                FROM document_identity
                GROUP BY project
                ORDER BY COUNT(*) DESC
                LIMIT 20
            """)

            rows = cursor.fetchall()

            print("\nProjects\n")

            for row in rows:
                print(row)

        except Exception as e:
            print(e)

    elif "document" in question.lower():

        try:
            cursor.execute("""
                SELECT title
                FROM documents
                LIMIT 20
            """)

            rows = cursor.fetchall()

            print("\nDocuments\n")

            for row in rows:
                print(row[0])

        except Exception as e:
            print(e)

    elif "memory" in question.lower():

        try:
            cursor.execute("""
                SELECT COUNT(*)
                FROM memories
            """)

            print(
                "\nMemories:",
                cursor.fetchone()[0]
            )

        except Exception as e:
            print(e)

    else:

        print(
            "Try: projects, documents, memories"
        )

conn.close()
