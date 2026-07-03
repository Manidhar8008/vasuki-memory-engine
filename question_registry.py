import sqlite3

QUESTIONS = [
    ("identity", "What entities are most central to Manidhar?"),
    ("identity", "What organizations shaped his career?"),
    ("identity", "What roles has he occupied?"),

    ("capabilities", "What technical capabilities appear most often?"),
    ("capabilities", "Which technologies are production tested?"),
    ("capabilities", "Which skills are growing?"),

    ("projects", "What projects are active?"),
    ("projects", "What projects are abandoned?"),
    ("projects", "Which project generated the most effort?"),
    ("projects", "What is Vasuki?"),
    ("projects", "What is Janani?"),

    ("founder", "What startups is he building?"),
    ("founder", "What market opportunities recur?"),
    ("founder", "What founder beliefs recur?"),

    ("decisions", "What major decisions occurred?"),
    ("decisions", "Which successful patterns repeated?"),
    ("decisions", "Which mistakes repeated?"),

    ("learning", "What topics is he studying?"),
    ("learning", "What recurring interests exist?"),

    ("operating_system", "What productivity systems recur?"),
    ("operating_system", "What bottlenecks recur?"),

    ("vasuki", "Why was Vasuki created?"),
    ("vasuki", "Which systems compose Vasuki?"),
    ("vasuki", "What capabilities does Vasuki possess?"),
    ("vasuki", "What is the roadmap of Vasuki?")
]

conn = sqlite3.connect("founder.db")
cur = conn.cursor()

for category, question in QUESTIONS:
    cur.execute(
        "INSERT OR IGNORE INTO founder_questions(category, question) VALUES (?, ?)",
        (category, question)
    )

conn.commit()
conn.close()

print(f"Seeded {len(QUESTIONS)} questions.")
