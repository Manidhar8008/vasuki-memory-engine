from database.db import get_db

def get_relationships():

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""
    SELECT
    concept_a,
    concept_b,
    weight
    FROM relationships
    ORDER BY weight DESC
    LIMIT 100
    """)

    rows = cur.fetchall()

    conn.close()

    return rows
