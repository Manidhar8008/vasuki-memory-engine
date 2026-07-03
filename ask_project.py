#!/usr/bin/env python3

import sqlite3
import sys
from pathlib import Path

DB = str(Path.home() / "vasuki" / "vasuki.db")

if len(sys.argv) < 2:
    print("Usage:")
    print("python ask_project.py Vasuki")
    exit()

project = " ".join(sys.argv[1:])

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("""
SELECT *
FROM project_profiles
WHERE lower(project_name)=lower(?)
""", (project,))

row = cur.fetchone()

if not row:
    print("Project not found")
    exit()

print("\n" + "="*50)
print("PROJECT PROFILE")
print("="*50)

print(f"\nName: {row['project_name']}")
print(f"Facts: {row['fact_count']}")
print(f"Evidence: {row['evidence_count']}")
print(f"Technologies: {row['technologies']}")
print(f"Confidence: {row['confidence']}")

print("\nSupporting Evidence\n")

cur.execute("""
SELECT evidence
FROM facts
WHERE object=?
LIMIT 10
""", (project,))

for r in cur.fetchall():
    print("-", str(r["evidence"])[:120])

conn.close()
