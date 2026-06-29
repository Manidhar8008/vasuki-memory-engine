from fastapi import FastAPI
import sqlite3

    app = FastAPI()

@app.get("/real-stats")
def real_stats():

    conn = sqlite3.connect("/path/to/vasuki.db")

    cur = conn.cursor()

    documents = cur.execute(
        "SELECT COUNT(*) FROM documents"
    ).fetchone()[0]

    entities = cur.execute(
        "SELECT COUNT(*) FROM entities"
    ).fetchone()[0]

    evidence = cur.execute(
        "SELECT COUNT(*) FROM evidence"
    ).fetchone()[0]

    conn.close()

    return {
        "documents": documents,
        "entities": entities,
        "evidence": evidence
    }
