from pathlib import Path
import sqlite3

DB_DIR = Path("memory")
DB_DIR.mkdir(exist_ok=True)

DB_FILE = DB_DIR / "vasuki.db"

conn = sqlite3.connect(DB_FILE)

conn.execute("""
CREATE TABLE IF NOT EXISTS memories(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    type TEXT,
    content TEXT,
    source TEXT,
    device TEXT,
    tags TEXT
)
""")

conn.commit()

print("Database Ready")
