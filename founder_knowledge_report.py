#!/usr/bin/env python3

import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = "vasuki.db"


def query_dict(cursor, sql):
    cursor.execute(sql)
    cols = [d[0] for d in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    projects = query_dict(cur, """
        SELECT object, COUNT(*) AS mentions
        FROM facts
        WHERE predicate='BUILT'
        GROUP BY object
        ORDER BY mentions DESC;
    """)

    skills = query_dict(cur, """
        SELECT object, COUNT(*) AS mentions
        FROM facts
        WHERE predicate='USES'
        GROUP BY object
        ORDER BY mentions DESC;
    """)

    goals = query_dict(cur, """
        SELECT truth
        FROM founder_truths
        WHERE truth_type='GOAL';
    """)

    learnings = query_dict(cur, """
        SELECT truth
        FROM founder_truths
        WHERE truth_type='LEARNING';
    """)

    decisions = query_dict(cur, """
        SELECT truth
        FROM founder_truths
        WHERE truth_type='DECISION';
    """)

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

    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "founder": "Manidhar",
        "database_stats": stats,
        "projects": projects,
        "skills": skills,
        "goals": goals,
        "learnings": learnings,
        "decisions": decisions,
    }

    Path("reports").mkdir(exist_ok=True)

    json_path = "reports/founder_knowledge_report.json"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    md_path = "reports/founder_knowledge_report.md"

    with open(md_path, "w", encoding="utf-8") as f:

        f.write("# Founder Knowledge Report\n\n")

        f.write(f"Generated: {report['generated_at']}\n\n")

        f.write("## Database Statistics\n\n")

        for k, v in stats.items():
            f.write(f"- **{k}**: {v}\n")

        f.write("\n## Top Projects\n\n")

        for p in projects:
            f.write(
                f"- {p['object']} ({p['mentions']} references)\n"
            )

        f.write("\n## Top Skills\n\n")

        for s in skills:
            f.write(
                f"- {s['object']} ({s['mentions']} references)\n"
            )

        f.write("\n## Goals\n\n")

        for g in goals:
            f.write(f"- {g['truth']}\n")

        f.write("\n## Decisions\n\n")

        for d in decisions:
            f.write(f"- {d['truth']}\n")

        f.write("\n## Learnings\n\n")

        for l in learnings:
            f.write(f"- {l['truth']}\n")

    print("=" * 60)
    print("VASUKI FOUNDER REPORT GENERATED")
    print("=" * 60)
    print(json_path)
    print(md_path)

    conn.close()


if __name__ == "__main__":
    main()
