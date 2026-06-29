from services.db import get_connection


def get_documents():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM documents"
    )

    count = cur.fetchone()[0]

    conn.close()

    return count


def get_evidence():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM founder_evidence"
    )

    count = cur.fetchone()[0]

    conn.close()

    return count


def get_entities():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM entities"
    )

    count = cur.fetchone()[0]

    conn.close()

    return count


def get_timeline():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM founder_timeline"
    )

    count = cur.fetchone()[0]

    conn.close()

    return count
