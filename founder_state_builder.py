import sqlite3
import json
from datetime import datetime

DB = "vasuki.db"

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

# ------------------------------------
# Create founder_state table
# ------------------------------------

conn.execute("""
CREATE TABLE IF NOT EXISTS founder_state (
    id INTEGER PRIMARY KEY,
    identity TEXT,
    projects TEXT,
    technologies TEXT,
    companies TEXT,
    locations TEXT,
    pets TEXT,
    generated_summary TEXT,
    updated_at TEXT
)
""")

# ------------------------------------
# Extract trusted entities
# ------------------------------------

def get_entities(entity_type):
    rows = conn.execute("""
    SELECT DISTINCT node_name
    FROM kg_nodes
    WHERE node_type = ?
    ORDER BY node_name
    """, (entity_type,)).fetchall()

    return [r["node_name"] for r in rows]

projects = get_entities("PROJECT")
technologies = get_entities("TECHNOLOGY")
companies = get_entities("COMPANY")
locations = get_entities("LOCATION")
pets = get_entities("PET")
people = get_entities("PERSON")

# ------------------------------------
# Determine identity
# ------------------------------------

identity = "Founder"

for p in people:
    if p.lower() == "manidhar":
        identity = (
            "AI Systems Builder focused on Personal Intelligence, "
            "Knowledge Graphs and AI Operating Systems"
        )

# ------------------------------------
# Generate recruiter summary
# ------------------------------------

summary = f"""
Manidhar is an AI systems builder and founder.

Current Projects:
{", ".join(projects)}

Technology Stack:
{", ".join(technologies)}

Professional Background:
{", ".join(companies)}

Location:
{", ".join(locations)}

Focus Areas:
Personal Intelligence Systems,
Knowledge Graphs,
AI Agents,
Founder Tooling.

This profile is automatically generated from evidence
inside the Vasuki knowledge system.
""".strip()

# ------------------------------------
# Store founder state
# ------------------------------------

conn.execute("DELETE FROM founder_state")

conn.execute("""
INSERT INTO founder_state
(
identity,
projects,
technologies,
companies,
locations,
pets,
generated_summary,
updated_at
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""",
(
identity,
json.dumps(projects),
json.dumps(technologies),
json.dumps(companies),
json.dumps(locations),
json.dumps(pets),
summary,
datetime.utcnow().isoformat()
))

conn.commit()

print("\n=== FOUNDER STATE UPDATED ===\n")
print(summary)

conn.close()
