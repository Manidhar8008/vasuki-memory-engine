import sqlite3

DB = "founder.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS founder_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    question TEXT UNIQUE
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS founder_truths (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER,
    answer TEXT,
    confidence REAL,
    evidence TEXT,
    source_tables TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS founder_evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    truth_id INTEGER,
    source_table TEXT,
    source_id TEXT,
    snippet TEXT
)
""")

conn.commit()
conn.close()

print("Founder schema created.")
