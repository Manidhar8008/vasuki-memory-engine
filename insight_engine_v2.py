#!/usr/bin/env python3

import sqlite3
import json
from pathlib import Path
from collections import Counter

DB = str(Path.home() / "vasuki" / "vasuki.db")

OUTPUT = Path("outputs")
OUTPUT.mkdir(exist_ok=True)

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()


def count(table):
    try:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        return cur.fetchone()[0]
    except:
        return 0


def get_top(category, limit=50):
    try:
        cur.execute("""
        SELECT content
        FROM classified_memories
        WHERE category=?
        """, (category,))
        rows = [r["content"][:150] for r in cur.fetchall()]
        c = Counter(rows)
        return [{"name": k, "count": v}
                for k, v in c.most_common(limit)]
    except:
        return []


def top_entities(limit=50):

    tables = [
        "entity_mentions",
        "entities"
    ]

    for table in tables:

        try:

            cur.execute(f"""
            SELECT entity_name,
                   COUNT(*) as freq
            FROM {table}
            GROUP BY entity_name
            ORDER BY freq DESC
            LIMIT ?
            """, (limit,))

            rows = cur.fetchall()

            if rows:
                return [
                    {
                        "name": r[0],
                        "count": r[1]
                    }
                    for r in rows
                ]

        except:
            pass

    return []


metrics = {

    "files": count("files"),
    "documents": count("documents"),
    "memories": count("memories"),
    "entities": count("entities"),
    "mentions": count("entity_mentions"),
    "screenshots": count("screenshots")
}

insights = {

    "metrics": metrics,

    "skills": get_top("skill"),

    "projects": get_top("project"),

    "goals": get_top("goal"),

    "companies": get_top("company"),

    "top_entities": top_entities()
}

with open(
    OUTPUT / "portfolio_metrics.json",
    "w"
) as f:
    json.dump(metrics, f, indent=2)

with open(
    OUTPUT / "insights.json",
    "w"
) as f:
    json.dump(insights, f, indent=2)

report = f"""
# Founder Intelligence Report

## Metrics

Files: {metrics['files']}
Documents: {metrics['documents']}
Memories: {metrics['memories']}
Entities: {metrics['entities']}
Mentions: {metrics['mentions']}
Screenshots: {metrics['screenshots']}

## Top Skills

"""

for s in insights["skills"][:20]:
    report += f"- {s['name']} ({s['count']})\n"

report += "\n## Top Projects\n"

for p in insights["projects"][:20]:
    report += f"- {p['name']} ({p['count']})\n"

report += "\n## Top Companies\n"

for c in insights["companies"][:20]:
    report += f"- {c['name']} ({c['count']})\n"

with open(
    OUTPUT / "founder_report.md",
    "w"
) as f:
    f.write(report)

print("\nPHASE 1 COMPLETE\n")

print(metrics)

conn.close()
