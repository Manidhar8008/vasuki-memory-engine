import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

topics = [
    "ai",
    "memory",
    "rag",
    "agent",
    "python",
    "automation",
    "psychology",
    "finance"
]

print("\n=== VASUKI KNOWLEDGE MAP ===\n")

for topic in topics:

    count = cur.execute(
        """
        SELECT COUNT(*)
        FROM documents
        WHERE LOWER(content) LIKE ?
        """,
        (f"%{topic}%",)
    ).fetchone()[0]

    print(f"{topic.upper()} : {count}")

conn.close()
