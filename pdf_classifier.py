import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

rows = cur.execute("""
SELECT title, content
FROM documents
""").fetchall()

CATEGORIES = {
    "AI": [
        "agent","llm","prompt",
        "rag","vector","embedding",
        "memory","model"
    ],

    "Finance": [
        "bank","loan","insurance",
        "tax","investment","salary"
    ],

    "Career": [
        "resume","cv",
        "interview","job"
    ],

    "Education": [
        "assignment","exam",
        "project","research"
    ]
}

for title,content in rows:

    text = (content or "").lower()

    scores = {}

    for category,words in CATEGORIES.items():

        score = sum(
            text.count(word)
            for word in words
        )

        scores[category] = score

    best = max(scores,key=scores.get)

    print()
    print(title)
    print("=>",best)
    print(scores)

conn.close()
