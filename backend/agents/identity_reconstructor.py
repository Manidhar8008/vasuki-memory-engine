from database.db import get_db

def profile():

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""
    SELECT
    title,
    COUNT(*)
    FROM timeline
    GROUP BY title
    ORDER BY COUNT(*) DESC
    """)

    rows = cur.fetchall()

    conn.close()

    return rows
