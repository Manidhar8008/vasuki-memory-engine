import sqlite3

DB="founder.db"

conn=sqlite3.connect(DB)

cur=conn.cursor()

for project in ["vasuki","mw.ai","janani"]:

    print("\n===================")
    print(project.upper())
    print("===================\n")

    cur.execute("""
    SELECT
    filename,
    mentions
    FROM project_evidence
    WHERE project=?
    ORDER BY mentions DESC
    """,(project,))

    rows=cur.fetchall()

    for row in rows:

        print(row[0],row[1])

conn.close()
