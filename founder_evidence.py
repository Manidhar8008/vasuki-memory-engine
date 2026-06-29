import sqlite3
import pandas as pd

DB = "vasuki.db"

KEYWORDS = [
    "vasuki",
    "janani",
    "ai",
    "agent",
    "startup",
    "python",
    "sql",
    "architecture",
    "portfolio",
    "founder",
    "machine learning",
    "data"
]

conn = sqlite3.connect(DB)

docs = pd.read_sql(
    """
    SELECT
        title,
        path
    FROM documents
    """,
    conn
)

print("\n=== FOUNDER EVIDENCE ===\n")

matches = []

for _, row in docs.iterrows():

    title = str(row["title"]).lower()

    for keyword in KEYWORDS:

        if keyword.lower() in title:

            matches.append({
                "keyword": keyword,
                "title": row["title"],
                "path": row["path"]
            })

evidence = pd.DataFrame(matches)

if len(evidence):
    print(evidence.to_string(index=False))
else:
    print("No evidence found")

conn.close()
