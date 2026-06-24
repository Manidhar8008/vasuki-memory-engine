import sqlite3
import sys

query = " ".join(sys.argv[1:])

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

print("="*80)
print("DOCUMENT SEARCH")
print("="*80)

try:
    cur.execute("""
    SELECT path
    FROM document_fts
    WHERE document_fts MATCH ?
    LIMIT 20
    """,(query,))

    for row in cur.fetchall():
        print(row[0])

except Exception as e:
    print(e)

print()
print("="*80)
print("MEMORY SEARCH")
print("="*80)

try:
    cur.execute("""
    SELECT memory
    FROM memory_fts
    WHERE memory_fts MATCH ?
    LIMIT 20
    """,(query,))

    for row in cur.fetchall():
        print()
        print(row[0][:500])

except Exception as e:
    print(e)

print()
print("="*80)
print("ENTITY SEARCH")
print("="*80)

try:
    cur.execute("""
    SELECT entity,
           frequency
    FROM entities
    WHERE entity LIKE ?
    ORDER BY frequency DESC
    LIMIT 20
    """,(f"%{query}%",))

    for row in cur.fetchall():
        print(row)

except Exception as e:
    print(e)

conn.close()
