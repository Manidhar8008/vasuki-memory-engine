import sqlite3
import sys

query = " ".join(sys.argv[1:])

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

print("="*80)
print("DOCUMENTS")
print("="*80)

cur.execute("""
SELECT path
FROM documents
WHERE content LIKE ?
LIMIT 20
""",(f"%{query}%",))

for row in cur.fetchall():
    print(row[0])

print()

print("="*80)
print("MEMORIES")
print("="*80)

cur.execute("""
SELECT memory
FROM memories
WHERE memory LIKE ?
LIMIT 20
""",(f"%{query}%",))

for row in cur.fetchall():
    print(row[0][:300])
    print()

print("="*80)
print("ENTITIES")
print("="*80)

cur.execute("""
SELECT entity,frequency
FROM entities
WHERE entity LIKE ?
ORDER BY frequency DESC
LIMIT 20
""",(f"%{query}%",))

for row in cur.fetchall():
    print(row)

conn.close()
