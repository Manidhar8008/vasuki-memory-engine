from database.db import get_db

def search(query):

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""
    SELECT title
    FROM documents
    WHERE lower(content) LIKE ?
    LIMIT 20
    """,
    (
        f"%{query.lower()}%",
    ))

    rows = cur.fetchall()

    conn.close()

    return rows
