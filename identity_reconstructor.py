import sqlite3

DB = "/data/data/com.termux/files/home/vasuki/vasuki.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

PROJECTS = [
    "vasuki",
    "mw.ai",
    "mw ai",
    "janani",
    "room os"
]

print("\n========================")
print("VASUKI IDENTITY REPORT")
print("========================\n")

for project in PROJECTS:

    cur.execute("""
    SELECT COUNT(*)
    FROM documents
    WHERE lower(content) LIKE ?
    """,
    (f"%{project}%",))

    docs = cur.fetchone()[0]

    cur.execute("""
    SELECT COUNT(*)
    FROM timeline
    WHERE lower(title)=?
    """,
    (project.upper(),))

    timeline_events = cur.fetchone()[0]

    print(f"PROJECT: {project}")
    print(f"DOCUMENTS: {docs}")
    print(f"TIMELINE EVENTS: {timeline_events}")
    print("-"*40)

conn.close()
