#!/usr/bin/env python3

import sqlite3
import json
from pathlib import Path

DB = str(Path.home() / "vasuki" / "vasuki.db")

PROJECTS = [
    "Vasuki",
    "Janani",
    "MW.AI",
    "Found the Unfindable",
    "Lime IoT ML Platform",
    "AI-powered Supply Chain Automation System"
]

TECH = [
    "Python",
    "FastAPI",
    "SQLite",
    "PostgreSQL",
    "React",
    "TypeScript",
    "Docker",
    "GitHub",
    "Qdrant",
    "Ollama"
]

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("DELETE FROM project_profiles")

for project in PROJECTS:

    cur.execute("""
    SELECT COUNT(*)
    FROM facts
    WHERE object = ?
    """, (project,))

    fact_count = cur.fetchone()[0]

    tech_found = []

    for tech in TECH:

        cur.execute("""
        SELECT COUNT(*)
        FROM facts
        WHERE object = ?
        """, (tech,))

        count = cur.fetchone()[0]

        if count > 0:
            tech_found.append(tech)

    cur.execute("""
    INSERT OR REPLACE INTO project_profiles(
        project_name,
        fact_count,
        technologies,
        confidence
    )
    VALUES(?,?,?,?)
    """, (
        project,
        fact_count,
        ",".join(tech_found),
        0.8
    ))

conn.commit()

cur.execute("""
SELECT *
FROM project_profiles
ORDER BY fact_count DESC
""")

rows = [dict(r) for r in cur.fetchall()]

Path("outputs").mkdir(exist_ok=True)

with open("outputs/project_profiles.json", "w") as f:
    json.dump(rows, f, indent=2)

print("\nPROJECT PROFILES CREATED\n")

for row in rows:
    print(
        f"{row['project_name']} -> "
        f"{row['fact_count']} facts"
    )

conn.close()

