import sqlite3

db = sqlite3.connect("vasuki.db")
cur = db.cursor()

goal_count = cur.execute("""
SELECT COUNT(*)
FROM ontology_objects
WHERE object_type='GOAL'
""").fetchone()[0]

project_count = cur.execute("""
SELECT COUNT(*)
FROM ontology_objects
WHERE object_type='PROJECT'
""").fetchone()[0]

decision_count = cur.execute("""
SELECT COUNT(*)
FROM ontology_objects
WHERE object_type='DECISION'
""").fetchone()[0]

failure_count = cur.execute("""
SELECT COUNT(*)
FROM ontology_objects
WHERE object_type='FAILURE'
""").fetchone()[0]

learning_count = cur.execute("""
SELECT COUNT(*)
FROM ontology_objects
WHERE object_type='LEARNING'
""").fetchone()[0]

print("\n=== FOUNDER EXECUTIVE SUMMARY ===\n")

print("Goals      :", goal_count)
print("Projects   :", project_count)
print("Decisions  :", decision_count)
print("Failures   :", failure_count)
print("Learnings  :", learning_count)
