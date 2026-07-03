#!/usr/bin/env python3

import sqlite3
from pathlib import Path

DB = str(Path.home() / "vasuki" / "vasuki.db")

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print("\n" + "="*70)
print("VASUKI DATABASE DEEP AUDIT")
print("="*70)

TABLES = [
    "files",
    "documents",
    "memories",
    "classified_memories",
    "entities",
    "entity_mentions",
    "ocr_records",
    "projects_v2",
    "skills_v2",
    "goals",
    "decisions",
    "observations",
    "graph",
    "timeline"
]

for table in TABLES:

    try:
        cur.execute(f"SELECT COUNT(*) c FROM {table}")
        count = cur.fetchone()["c"]

        print(f"\n[{table}]")
        print(f"rows = {count}")

        cur.execute(f"PRAGMA table_info({table})")
        cols = [r[1] for r in cur.fetchall()]

        print("columns:")
        print(", ".join(cols))

        text_col = None

        for c in cols:
            if c.lower() in [
                "content",
                "memory",
                "text",
                "title",
                "name",
                "entity_name"
            ]:
                text_col = c
                break

        if text_col:

            try:
                cur.execute(
                    f"""
                    SELECT {text_col}
                    FROM {table}
                    WHERE {text_col} IS NOT NULL
                    LIMIT 5
                    """
                )

                rows = cur.fetchall()

                print("\nsamples:")

                for r in rows:
                    print("-" + str(r[0])[:120])

            except:
                pass

    except Exception as e:
        print(table, e)

print("\n" + "="*70)

# TOP ENTITY TYPES

try:

    cur.execute("""
    SELECT entity_type,
           COUNT(*) freq
    FROM entities
    GROUP BY entity_type
    ORDER BY freq DESC
    LIMIT 20
    """)

    print("\nTOP ENTITY TYPES\n")

    for r in cur.fetchall():
        print(r["entity_type"], r["freq"])

except:
    print("No entity_type column")

print("\n" + "="*70)

# TOP PROJECTS

try:

    cur.execute("""
    SELECT name,
           COUNT(*) freq
    FROM projects_v2
    GROUP BY lower(name)
    ORDER BY freq DESC
    LIMIT 20
    """)

    print("\nTOP PROJECTS\n")

    for r in cur.fetchall():
        print(r["freq"], r["name"][:80])

except:
    pass

print("\n" + "="*70)

# TOP SKILLS

try:

    cur.execute("""
    SELECT name,
           COUNT(*) freq
    FROM skills_v2
    GROUP BY lower(name)
    ORDER BY freq DESC
    LIMIT 20
    """)

    print("\nTOP SKILLS\n")

    for r in cur.fetchall():
        print(r["freq"], r["name"][:80])

except:
    pass

conn.close()

print("\nAUDIT COMPLETE\n")
