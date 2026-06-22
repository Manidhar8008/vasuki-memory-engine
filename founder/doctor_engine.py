import sqlite3
from datetime import datetime

DB="founder.db"

conn=sqlite3.connect(DB)
cur=conn.cursor()

PROJECTS=["vasuki","mw.ai","janani"]

for project in PROJECTS:

    cur.execute("""
    SELECT COUNT(*)
    FROM founder_artifacts
    WHERE lower(filename)
    LIKE ?
    """,("%"+project.lower()+"%",))

    file_count=cur.fetchone()[0]

    cur.execute("""
    SELECT COUNT(*)
    FROM project_evidence
    WHERE lower(project)
    = ?
    """,(project.lower(),))

    row=cur.fetchone()

    mentions=0

    if row:
        mentions=row[0]

    energy=(file_count*5)+(mentions*2)

    momentum=min(
        energy,
        100
    )

    health=min(
        100,
        50+(file_count*2)
    )

    cur.execute("""
    UPDATE doctor_projects

    SET

    energy_score=?,
    momentum_score=?,
    health_score=?,
    evidence_count=?,
    last_seen=?

    WHERE lower(name)=?
    """,
    (
        energy,
        momentum,
        health,
        file_count,
        datetime.now().isoformat(),
        project.lower()
    ))

conn.commit()

conn.close()

print("DOCTOR COMPLETE")

