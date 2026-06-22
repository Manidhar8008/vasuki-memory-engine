import sqlite3

DB="founder.db"

conn=sqlite3.connect(DB)
cur=conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS doctor_reports(
id INTEGER PRIMARY KEY,
entity_type TEXT,
entity_name TEXT,
energy INTEGER,
evidence_count INTEGER,
status TEXT
)
""")

cur.execute("""
DELETE FROM doctor_reports
""")

# PROJECTS

try:

    cur.execute("""
    SELECT
    project,
    SUM(mentions)
    FROM project_evidence
    GROUP BY project
    """)

    for project,mentions in cur.fetchall():

        energy = mentions * 10

        status = "ALIVE"

        if energy < 20:
            status = "WEAK"

        cur.execute("""
        INSERT INTO doctor_reports(
        entity_type,
        entity_name,
        energy,
        evidence_count,
        status
        )
        VALUES(?,?,?,?,?)
        """,(
            "PROJECT",
            project,
            energy,
            mentions,
            status
        ))

except:
    pass

# TOOLS

try:

    cur.execute("""
    SELECT
    name
    FROM tools
    """)

    for (tool,) in cur.fetchall():

        cur.execute("""
        INSERT INTO doctor_reports(
        entity_type,
        entity_name,
        energy,
        evidence_count,
        status
        )
        VALUES(?,?,?,?,?)
        """,(
            "TOOL",
            tool,
            50,
            1,
            "ACTIVE"
        ))

except:
    pass

# REPOS

try:

    cur.execute("""
    SELECT
    repo,
    COUNT(*)
    FROM github_artifacts
    GROUP BY repo
    """)

    for repo,count in cur.fetchall():

        cur.execute("""
        INSERT INTO doctor_reports(
        entity_type,
        entity_name,
        energy,
        evidence_count,
        status
        )
        VALUES(?,?,?,?,?)
        """,(
            "REPOSITORY",
            repo,
            count,
            count,
            "INDEXED"
        ))

except:
    pass

conn.commit()

print("DOCTOR REPORT GENERATED")

conn.close()
