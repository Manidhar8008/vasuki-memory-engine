import sqlite3
import sys

conn = sqlite3.connect("vasuki.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

question = " ".join(sys.argv[1:]).lower()

if not question:
    print("Usage:")
    print('python ask_truth.py "What is Manidhar building?"')
    exit()

print("\n" + "="*80)
print("VASUKI TRUTH ENGINE")
print("="*80)

# --------------------------------------------------
# PROJECT QUESTIONS
# --------------------------------------------------

if any(x in question for x in [
    "building",
    "project",
    "startup",
    "working on"
]):

    cur.execute("""
    SELECT truth
    FROM founder_truths
    WHERE truth_type='PROJECT'
    ORDER BY confidence DESC
    """)

    rows = cur.fetchall()

    print("\nCURRENT PROJECTS:\n")

    for r in rows:
        print("-", r["truth"])

# --------------------------------------------------
# GOAL QUESTIONS
# --------------------------------------------------

elif any(x in question for x in [
    "goal",
    "future",
    "want",
    "achieve",
    "target"
]):

    cur.execute("""
    SELECT truth
    FROM founder_truths
    WHERE truth_type='GOAL'
    ORDER BY confidence DESC
    """)

    rows = cur.fetchall()

    print("\nFOUNDER GOALS:\n")

    for r in rows:
        print("-", r["truth"])

# --------------------------------------------------
# FAILURE QUESTIONS
# --------------------------------------------------

elif any(x in question for x in [
    "mistake",
    "failure",
    "wrong",
    "problem"
]):

    cur.execute("""
    SELECT truth
    FROM founder_truths
    WHERE truth_type='FAILURE'
    ORDER BY confidence DESC
    """)

    rows = cur.fetchall()

    print("\nKNOWN FAILURES:\n")

    for r in rows:
        print("-", r["truth"])

# --------------------------------------------------
# DECISION QUESTIONS
# --------------------------------------------------

elif any(x in question for x in [
    "decision",
    "choose",
    "architecture",
    "why"
]):

    cur.execute("""
    SELECT truth
    FROM founder_truths
    WHERE truth_type='DECISION'
    ORDER BY confidence DESC
    """)

    rows = cur.fetchall()

    print("\nKEY DECISIONS:\n")

    for r in rows:
        print("-", r["truth"])

# --------------------------------------------------
# LEARNING QUESTIONS
# --------------------------------------------------

elif any(x in question for x in [
    "learn",
    "lesson",
    "insight",
    "realize"
]):

    cur.execute("""
    SELECT truth
    FROM founder_truths
    WHERE truth_type='LEARNING'
    ORDER BY confidence DESC
    """)

    rows = cur.fetchall()

    print("\nFOUNDER LEARNINGS:\n")

    for r in rows:
        print("-", r["truth"])

# --------------------------------------------------
# GENERAL
# --------------------------------------------------

else:

    cur.execute("""
    SELECT truth_type,truth
    FROM founder_truths
    ORDER BY confidence DESC
    LIMIT 20
    """)

    rows = cur.fetchall()

    print("\nMOST IMPORTANT TRUTHS:\n")

    for r in rows:
        print(f"[{r['truth_type']}] {r['truth']}")

conn.close()
