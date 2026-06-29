import sqlite3

DB="vasuki.db"

PROJECTS = [
    "vasuki",
    "janani",
    "mw.ai",
    "aim1000"
]

GOAL_WORDS = [
    "goal",
    "target",
    "roadmap",
    "objective",
    "want to",
    "need to"
]

DECISION_WORDS = [
    "decided",
    "decision",
    "choose",
    "selected",
    "going with"
]

FAILURE_WORDS = [
    "failed",
    "failure",
    "mistake",
    "problem",
    "stuck",
    "issue"
]

LEARNING_WORDS = [
    "learned",
    "lesson",
    "insight",
    "realized",
    "understood"
]


def classify(text):

    t = text.lower()

    for p in PROJECTS:
        if p in t:
            return "PROJECT"

    for w in GOAL_WORDS:
        if w in t:
            return "GOAL"

    for w in DECISION_WORDS:
        if w in t:
            return "DECISION"

    for w in FAILURE_WORDS:
        if w in t:
            return "FAILURE"

    for w in LEARNING_WORDS:
        if w in t:
            return "LEARNING"

    return None


conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
SELECT id,memory
FROM memories
""")

rows = cur.fetchall()

count = 0

for mem_id,text in rows:

    if not text:
        continue

    category = classify(text)

    if not category:
        continue

    cur.execute("""
    INSERT INTO ontology_objects(
        object_type,
        name,
        description,
        source_table,
        source_id,
        confidence
    )
    VALUES(?,?,?,?,?,?)
    """,(
        category,
        text[:120],
        text,
        "memories",
        mem_id,
        0.8
    ))

    count += 1

conn.commit()

print("CREATED:",count)
