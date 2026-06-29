import sqlite3

DB="vasuki.db"

def search_memories(q):

    conn=sqlite3.connect(DB)
    cur=conn.cursor()

    rows=cur.execute("""
    SELECT memory
    FROM memories
    WHERE memory LIKE ?
    LIMIT 30
    """,('%'+q+'%',)).fetchall()

    conn.close()

    return [r[0] for r in rows]

def search_everything(query):

    conn=sqlite3.connect(DB)
    cur=conn.cursor()

    docs=cur.execute("""
    SELECT path
    FROM documents
    WHERE content LIKE ?
    LIMIT 20
    """,('%'+query+'%',)).fetchall()

    mems=cur.execute("""
    SELECT memory
    FROM memories
    WHERE memory LIKE ?
    LIMIT 20
    """,('%'+query+'%',)).fetchall()

    ents=cur.execute("""
    SELECT entity
    FROM entities
    WHERE entity LIKE ?
    LIMIT 20
    """,('%'+query+'%',)).fetchall()

    conn.close()

	return docs,mems,ents
