import sqlite3
from datetime import datetime

DB = "vasuki.db"

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

# -------------------------
# helpers
# -------------------------

def scalar(sql):
    row = conn.execute(sql).fetchone()
    return row[0] if row else 0

def rows(sql):
    return conn.execute(sql).fetchall()

# -------------------------
# reset outputs
# -------------------------

conn.execute("DELETE FROM founder_state")
conn.execute("DELETE FROM founder_patterns")
conn.execute("DELETE FROM founder_insights")

# -------------------------
# STATE
# -------------------------

project_count = scalar("""
SELECT COUNT(*)
FROM kg_nodes
WHERE node_type='PROJECT'
""")

technology_count = scalar("""
SELECT COUNT(*)
FROM kg_nodes
WHERE node_type='TECHNOLOGY'
""")

company_count = scalar("""
SELECT COUNT(*)
FROM kg_nodes
WHERE node_type='COMPANY'
""")

document_count = scalar("""
SELECT COUNT(*)
FROM documents
""")

memory_count = scalar("""
SELECT COUNT(*)
FROM memories
""")

concept_count = scalar("""
SELECT COUNT(*)
FROM concepts
""")

states = [
    ("builder", project_count * 10),
    ("engineering", technology_count * 10),
    ("career", company_count * 10),
    ("knowledge", document_count / 20),
    ("memory", memory_count / 20),
    ("research", concept_count / 100),
]

for state_name, score in states:
    conn.execute("""
    INSERT INTO founder_state
    (state_name, score, evidence_count)
    VALUES (?, ?, ?)
    """, (state_name, score, int(score)))

# -------------------------
# PATTERNS
# -------------------------

patterns = []

techs = rows("""
SELECT node_name
FROM kg_nodes
WHERE node_type='TECHNOLOGY'
""")

for t in techs:
    patterns.append(
        (
            "technology",
            t["node_name"],
            1,
            1.0
        )
    )

projects = rows("""
SELECT node_name
FROM kg_nodes
WHERE node_type='PROJECT'
""")

for p in projects:
    patterns.append(
        (
            "project",
            p["node_name"],
            1,
            1.0
        )
    )

for pattern in patterns:
    conn.execute("""
    INSERT INTO founder_patterns
    (
        pattern_type,
        pattern_name,
        occurrences,
        confidence
    )
    VALUES (?, ?, ?, ?)
    """, pattern)

# -------------------------
# INSIGHTS
# -------------------------

project_names = [
    r["node_name"]
    for r in projects
]

technology_names = [
    r["node_name"]
    for r in techs
]

insights = [

(
"identity",
"Founder Profile",
f"""
Manidhar appears to be a founder and AI systems builder.
Current projects include:
{", ".join(project_names)}.
"""
),

(
"technology",
"Technology Stack",
f"""
Primary technologies detected:
{", ".join(technology_names)}.
"""
),

(
"focus",
"Current Focus",
f"""
Evidence suggests focus on
AI systems,
knowledge management,
automation,
and software engineering.
"""
),

]

for insight_type, title, content in insights:

    conn.execute("""
    INSERT INTO founder_insights
    (
        insight_type,
        title,
        content,
        confidence,
        source_count,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        insight_type,
        title,
        content.strip(),
        0.9,
        len(project_names) + len(technology_names),
        datetime.utcnow().isoformat()
    ))

# -------------------------
# TIMELINE
# -------------------------

conn.execute("""
INSERT INTO founder_timeline
(
event_date,
event_type,
title,
source,
importance
)
VALUES
(
?,
'FOUNDER_MODEL_REFRESH',
'Founder model rebuilt',
'founder_update_engine',
10
)
""",
(datetime.utcnow().isoformat(),)
)

conn.commit()

print("\n=== DONE ===")

print("\nFounder State")
for r in rows("SELECT * FROM founder_state"):
    print(dict(r))

print("\nFounder Insights")
for r in rows("SELECT title FROM founder_insights"):
    print(dict(r))

conn.close()
