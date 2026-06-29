import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

cur.execute("""
SELECT id,memory
FROM memories
""")

rows = cur.fetchall()

goals = 0
decisions = 0
learnings = 0
failures = 0

for mid,text in rows:

    text = str(text or "")
    lower = text.lower()

    # GOALS
    if any(x in lower for x in [
        "goal",
        "target",
        "objective",
        "mission",
        "plan"
    ]):

        cur.execute("""
        INSERT INTO goals(
        title,
        status,
        priority,
        created_at
        )
        VALUES(?,?,?,datetime('now'))
        """,(
            text[:200],
            "active",
            1
        ))

        goals += 1

    # DECISIONS
    if any(x in lower for x in [
        "decided",
        "decision",
        "chosen",
        "selected"
    ]):

        cur.execute("""
        INSERT INTO decisions(
        decision,
        reason,
        created_at
        )
        VALUES(?,?,datetime('now'))
        """,(
            text[:300],
            ""
        ))

        decisions += 1

    # LEARNINGS
    if any(x in lower for x in [
        "learned",
        "lesson",
        "realized",
        "insight",
        "discovered"
    ]):

        cur.execute("""
        INSERT INTO learnings(
        learning,
        source,
        created_at
        )
        VALUES(?,?,datetime('now'))
        """,(
            text[:500],
            "memory"
        ))

        learnings += 1

    # FAILURES
    if any(x in lower for x in [
        "failed",
        "failure",
        "mistake",
        "lost",
        "wrong"
    ]):

        cur.execute("""
        INSERT INTO failures(
        failure,
        lesson,
        created_at
        )
        VALUES(?,?,datetime('now'))
        """,(
            text[:500],
            ""
        ))

        failures += 1

conn.commit()

print("\n=== EXTRACTION COMPLETE ===")
print("GOALS:", goals)
print("DECISIONS:", decisions)
print("LEARNINGS:", learnings)
print("FAILURES:", failures)

conn.close()
