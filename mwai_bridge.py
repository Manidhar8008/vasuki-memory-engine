from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

DB = "/data/data/com.termux/files/home/vasuki/vasuki.db"

app = FastAPI()


class AskRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "service": "MW.AI",
        "status": "running"
    }


@app.get("/health")
def health():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    files = cur.execute(
        "SELECT COUNT(*) FROM files"
    ).fetchone()[0]

    documents = cur.execute(
        "SELECT COUNT(*) FROM documents"
    ).fetchone()[0]

    memories = cur.execute(
        "SELECT COUNT(*) FROM memories"
    ).fetchone()[0]

    conn.close()

    return {
        "files": files,
        "documents": documents,
        "memories": memories
    }


@app.get("/search")
def search(q: str):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    rows = cur.execute(
        """
        SELECT
            title,
            category,
            substr(content,1,500) as preview
        FROM documents
        WHERE
            lower(title) LIKE lower(?)
            OR lower(content) LIKE lower(?)
        LIMIT 20
        """,
        (f"%{q}%", f"%{q}%")
    ).fetchall()

    conn.close()

    return {
        "query": q,
        "count": len(rows),
        "results": [dict(r) for r in rows]
    }


@app.post("/ask")
def ask(req: AskRequest):

    q = req.question

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    rows = cur.execute(
        """
        SELECT
            title,
            category,
            substr(content,1,1500) as content
        FROM documents
        WHERE
            lower(title) LIKE lower(?)
            OR lower(content) LIKE lower(?)
        LIMIT 10
        """,
        (f"%{q}%", f"%{q}%")
    ).fetchall()

    conn.close()

    return {
        "question": q,
        "matches": len(rows),
        "documents": [dict(r) for r in rows]
    }
