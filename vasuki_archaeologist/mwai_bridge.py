from fastapi import FastAPI
from contextlib import closing
import sqlite3

DB = "/data/data/com.termux/files/home/vasuki/vasuki.db"

app = FastAPI(title="MW.AI Core")

def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def root():
    return {
        "name": "MW.AI Core",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/stats")
def stats():

    with closing(get_conn()) as conn:
        cur = conn.cursor()

        data = {}

        tables = [
            "files",
            "documents",
            "concepts",
            "memories",
            "relationships",
            "entities",
            "timeline",
            "screenshots"
        ]

        for table in tables:
            try:
                data[table] = cur.execute(
                    f"SELECT COUNT(*) FROM {table}"
                ).fetchone()[0]
            except:
                data[table] = 0

        return data


@app.get("/files")
def files(limit: int = 100):

    with closing(get_conn()) as conn:

        rows = conn.execute("""
            SELECT *
            FROM files
            LIMIT ?
        """, (limit,)).fetchall()

        return {
            "count": len(rows),
            "results": [dict(r) for r in rows]
        }


@app.get("/documents")
def documents(limit: int = 50):

    with closing(get_conn()) as conn:

        rows = conn.execute("""
            SELECT
                title,
                category,
                chars
            FROM documents
            LIMIT ?
        """, (limit,)).fetchall()

        return {
            "count": len(rows),
            "results": [dict(r) for r in rows]
        }


@app.get("/concepts")
def concepts(limit: int = 100):

    with closing(get_conn()) as conn:

        rows = conn.execute("""
            SELECT *
            FROM concepts
            ORDER BY frequency DESC
            LIMIT ?
        """, (limit,)).fetchall()

        return {
            "count": len(rows),
            "results": [dict(r) for r in rows]
        }


@app.get("/memories")
def memories(limit: int = 50):

    with closing(get_conn()) as conn:

        rows = conn.execute("""
            SELECT *
            FROM memories
            LIMIT ?
        """, (limit,)).fetchall()

        return {
            "count": len(rows),
            "results": [dict(r) for r in rows]
        }


@app.get("/timeline")
def timeline(limit: int = 100):

    with closing(get_conn()) as conn:

        rows = conn.execute("""
            SELECT *
            FROM timeline
            LIMIT ?
        """, (limit,)).fetchall()

        return {
            "count": len(rows),
            "results": [dict(r) for r in rows]
        }


@app.get("/photos")
def photos(limit: int = 100):

    with closing(get_conn()) as conn:

        rows = conn.execute("""
            SELECT *
            FROM files
            WHERE extension IN
            (
                '.jpg',
                '.jpeg',
                '.png',
                '.webp',
                '.heic'
            )
            LIMIT ?
        """, (limit,)).fetchall()

        return {
            "count": len(rows),
            "results": [dict(r) for r in rows]
        }


@app.get("/videos")
def videos(limit: int = 100):

    with closing(get_conn()) as conn:

        rows = conn.execute("""
            SELECT *
            FROM files
            WHERE extension IN
            (
                '.mp4',
                '.mov',
                '.mkv'
            )
            LIMIT ?
        """, (limit,)).fetchall()

        return {
            "count": len(rows),
            "results": [dict(r) for r in rows]
        }


@app.get("/audio")
def audio(limit: int = 100):

    with closing(get_conn()) as conn:

        rows = conn.execute("""
            SELECT *
            FROM files
            WHERE extension IN
            (
                '.mp3',
                '.opus',
                '.wav'
            )
            LIMIT ?
        """, (limit,)).fetchall()

        return {
            "count": len(rows),
            "results": [dict(r) for r in rows]
        }


@app.get("/search")
def search(q: str):

    with closing(get_conn()) as conn:

        rows = conn.execute("""
            SELECT
                title,
                category,
                substr(content,1,500) AS preview
            FROM documents
            WHERE lower(content) LIKE lower(?)
            LIMIT 20
        """, (f"%{q}%",)).fetchall()

        return {
            "query": q,
            "count": len(rows),
            "results": [dict(r) for r in rows]
        }
