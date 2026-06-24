import sqlite3
import re
from datetime import datetime

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

print("=== VASUKI ARCHAEOLOGIST V2 ===")

rows = cur.execute("""
SELECT id,memory
FROM memories
""").fetchall()

goals = 0
projects = 0
decisions = 0
failures = 0
learnings = 0

for mid,text in rows:

    if not text:
        continue

    t = text.lower()

    # GOALS
    if any(x in t for x in [
        "goal",
        "target",
        "need to",
        "want to",
        "plan to",
        "mission"
    ]):

        cur.execute("""
        INSERT INTO goals(
            title,
            status,
            priority,
            created_at
        )
        VALUES(?,?,?,?)
        """,(
            text[:120],
            "active",
            5,
            datetime.now().isoformat()
        ))

        goals += 1

    # PROJECTS
    if any(x in t for x in [
        "project",
        "vasuki",
        "janani",
        "mw.ai",
        "startup",
        "system"
    ]):

        cur.execute("""
        INSERT INTO projects(
            name,
            status,
            description
        )
        VALUES(?,?,?)
        """,(
            text[:80],
            "active",
            text
        ))

        projects += 1

    # DECISIONS
    if any(x in t for x in [
        "decided",
        "decision",
        "chose",
        "choose",
        "selected"
    ]):

        cur.execute("""
        INSERT INTO decisions(
            decision,
            reason,
            created_at
        )
        VALUES(?,?,?)
        """,(
            text,
            "auto-extracted",
            datetime.now().isoformat()
        ))

        decisions += 1

    # FAILURES
    if any(x in t for x in [
        "failed",
        "failure",
        "mistake",
        "problem",
        "issue",
        "error"
    ]):

        cur.execute("""
        INSERT INTO failures(
            failure,
            lesson,
            created_at
        )
        VALUES(?,?,?)
        """,(
            text,
            "pending extraction",
            datetime.now().isoformat()
        ))

        failures += 1

    # LEARNINGS
    if any(x in t for x in [
        "learned",
        "learnt",
        "lesson",
        "insight",
        "realized",
        "discovered"
    ]):

        cur.execute("""
        INSERT INTO learnings(
            learning,
            source,
            created_at
        )
        VALUES(?,?,?)
        """,(
            text,
            "memory",
            datetime.now().isoformat()
        ))

        learnings += 1

conn.commit()

print()
print("GOALS:",goals)
print("PROJECTS:",projects)
print("DECISIONS:",decisions)
print("FAILURES:",failures)
print("LEARNINGS:",learnings)

conn.close()
