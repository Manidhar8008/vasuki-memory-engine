#!/usr/bin/env python3

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

DB_PATH = "vasuki.db"

app = FastAPI(
    title="Vasuki Explorer API",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    query: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def search_memories(query: str, limit: int = 5):

    conn = get_db()

    rows = conn.execute(
        """
        SELECT
            memory,
            confidence,
            memory_type,
            category
        FROM memories
        WHERE rowid IN (
            SELECT rowid
            FROM memory_fts
            WHERE memory_fts MATCH ?
        )
        ORDER BY confidence DESC
        LIMIT ?
        """,
        (query, limit)
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def search_documents(query: str, limit: int = 5):

    conn = get_db()

    rows = conn.execute(
        """
        SELECT
            title,
            path,
            content,
            category
        FROM documents
        WHERE rowid IN (
            SELECT rowid
            FROM document_fts
            WHERE document_fts MATCH ?
        )
        LIMIT ?
        """,
        (query, limit)
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


@app.get("/")
def root():
    return {
        "name": "Vasuki Explorer API",
        "status": "running"
    }


@app.get("/api/founder/summary")
def founder_summary():

    conn = get_db()
    cur = conn.cursor()

    stats = {
        "documents": cur.execute(
            "SELECT COUNT(*) FROM documents"
        ).fetchone()[0],

        "memories": cur.execute(
            "SELECT COUNT(*) FROM memories"
        ).fetchone()[0],

        "facts": cur.execute(
            "SELECT COUNT(*) FROM facts"
        ).fetchone()[0],

        "knowledge_assets": cur.execute(
            "SELECT COUNT(*) FROM knowledge_assets"
        ).fetchone()[0],

        "founder_truths": cur.execute(
            "SELECT COUNT(*) FROM founder_truths"
        ).fetchone()[0],
    }

    conn.close()

    return stats


@app.get("/api/founder/projects")
def projects():

    conn = get_db()

    rows = conn.execute("""
        SELECT
            object,
            COUNT(*) as mentions
        FROM facts
        WHERE predicate='BUILT'
        GROUP BY object
        ORDER BY mentions DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


@app.get("/api/founder/skills")
def skills():

    conn = get_db()

    rows = conn.execute("""
        SELECT
            object,
            COUNT(*) as mentions
        FROM facts
        WHERE predicate='USES'
        GROUP BY object
        ORDER BY mentions DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


@app.get("/api/founder/goals")
def goals():

    conn = get_db()

    rows = conn.execute("""
        SELECT truth
        FROM founder_truths
        WHERE truth_type='GOAL'
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


@app.get("/api/founder/decisions")
def decisions():

    conn = get_db()

    rows = conn.execute("""
        SELECT truth
        FROM founder_truths
        WHERE truth_type='DECISION'
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


@app.get("/api/founder/learnings")
def learnings():

    conn = get_db()

    rows = conn.execute("""
        SELECT truth
        FROM founder_truths
        WHERE truth_type='LEARNING'
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


@app.get("/api/founder/timeline")
def timeline():

    conn = get_db()

    rows = conn.execute("""
        SELECT
            truth_type,
            truth,
            confidence,
            evidence_count
        FROM founder_truths
        ORDER BY evidence_count DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


@app.get("/api/founder/dashboard")
def dashboard():

    conn = get_db()

    projects = conn.execute("""
        SELECT object, COUNT(*) as mentions
        FROM facts
        WHERE predicate='BUILT'
        GROUP BY object
        ORDER BY mentions DESC
        LIMIT 10
    """).fetchall()

    skills = conn.execute("""
        SELECT object, COUNT(*) as mentions
        FROM facts
        WHERE predicate='USES'
        GROUP BY object
        ORDER BY mentions DESC
        LIMIT 10
    """).fetchall()

    goals = conn.execute("""
        SELECT truth
        FROM founder_truths
        WHERE truth_type='GOAL'
    """).fetchall()

    conn.close()

    return {
        "projects": [dict(x) for x in projects],
        "skills": [dict(x) for x in skills],
        "goals": [dict(x) for x in goals]
    }

@app.get("/api/stats")
def stats():

    conn = get_db()

    tables = [
        "documents",
        "memories",
        "concepts",
        "entities",
        "relationships",
        "timeline"
    ]

    result = {}

    for table in tables:
        try:
            count = conn.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

            result[table] = count

        except Exception as e:
            result[table] = str(e)

    conn.close()

    return result

@app.post("/api/query")
def query(request: QueryRequest):

    memories = search_memories(
        request.query,
        limit=5
    )

    documents = search_documents(
        request.query,
        limit=5
    )

    return {
        "query": request.query,
        "memories": memories,
        "documents": documents
    }

@app.get("/api/graph")
def get_graph():

    conn = get_db()

    nodes = conn.execute("""
        SELECT
            id,
            node_type,
            node_name,
            metadata
        FROM kg_nodes
    """).fetchall()

    edges = conn.execute("""
        SELECT
            id,
            source_node,
            target_node,
            relation,
            weight
        FROM kg_edges
    """).fetchall()

    conn.close()

    return {
        "nodes": [dict(row) for row in nodes],
        "edges": [dict(row) for row in edges],
        "node_count": len(nodes),
        "edge_count": len(edges)
    }

@app.get("/api/graph")
def get_graph():

    conn = get_db()

    nodes = conn.execute("""
        SELECT
            id,
            node_type,
            node_name,
            metadata
        FROM kg_nodes
        ORDER BY node_name
    """).fetchall()

    edges = conn.execute("""
        SELECT
            id,
            source_node,
            target_node,
            relation,
            weight
        FROM kg_edges
    """).fetchall()

    conn.close()

    return {
        "nodes": [dict(row) for row in nodes],
        "edges": [dict(row) for row in edges],
        "node_count": len(nodes),
        "edge_count": len(edges)
    }
@app.get("/api/node/{node_name}")
def get_node(node_name: str):

    conn = get_db()

    node = conn.execute("""
        SELECT *
        FROM kg_nodes
        WHERE node_name = ?
    """, (node_name,)).fetchone()

    if not node:
        conn.close()
        return {
            "error": "Node not found"
        }

    outgoing = conn.execute("""
        SELECT *
        FROM kg_edges
        WHERE source_node = ?
    """, (node_name,)).fetchall()

    incoming = conn.execute("""
        SELECT *
        FROM kg_edges
        WHERE target_node = ?
    """, (node_name,)).fetchall()

    conn.close()

    return {
        "node": dict(node),
        "outgoing": [dict(row) for row in outgoing],
        "incoming": [dict(row) for row in incoming]
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "explorer_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
