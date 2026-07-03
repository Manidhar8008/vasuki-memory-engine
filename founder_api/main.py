from fastapi import FastAPI
import sqlite3

app = FastAPI()

DB_PATH = "/data/data/com.termux/files/home/vasuki/vasuki_archaeologist/founder/founder.db"


@app.get("/")
def root():
    return {"status": "vasuki_online"}


@app.get("/stats")
def stats():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    result = {}

    tables = [
        "founder_entities",
        "observations",
        "memories",
        "identity_nodes",
        "identity_edges"
    ]

    for table in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            result[table] = cur.fetchone()[0]
        except:
            result[table] = 0

    conn.close()

    return result

