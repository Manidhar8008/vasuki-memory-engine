import sqlite3
import os
from pathlib import Path
from datetime import datetime

DB_NAME = "vasuki.db"
ROOT = "/storage/emulated/0"

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT UNIQUE,
    name TEXT,
    extension TEXT,
    category TEXT,
    size INTEGER,
    created_at TEXT,
    modified_at TEXT
)
""")

def classify_file(path, ext):
    p = path.lower()

    if "screenshot" in p:
        return "SCREENSHOT"

    if "screenrecord" in p or "recordings" in p:
        return "SCREEN_RECORDING"

    if ext in [".jpg", ".jpeg", ".png", ".webp"]:
        return "IMAGE"

    if ext in [".mp4", ".mkv", ".avi"]:
        return "VIDEO"

    if ext in [".mp3", ".aac", ".wav"]:
        return "AUDIO"

    if ext == ".pdf":
        return "PDF"

    if ext in [".py", ".js", ".ts", ".java", ".sql"]:
        return "CODE"

    if ext in [".doc", ".docx", ".txt", ".md"]:
        return "DOCUMENT"

    return "OTHER"

count = 0

for file in Path(ROOT).rglob("*"):
    try:
        if file.is_file():

            stat = os.stat(file)

            extension = file.suffix.lower()

            category = classify_file(
                str(file),
                extension
            )

            cur.execute("""
            INSERT OR IGNORE INTO files (
                path,
                name,
                extension,
                category,
                size,
                created_at,
                modified_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(file),
                file.name,
                extension,
                category,
                stat.st_size,
                datetime.fromtimestamp(
                    stat.st_ctime
                ).isoformat(),
                datetime.fromtimestamp(
                    stat.st_mtime
                ).isoformat()
            ))

            count += 1

            if count % 1000 == 0:
                print(f"Indexed {count}")

    except Exception:
        pass

conn.commit()
conn.close()

print(f"\nFinished indexing {count} files")
print("Database: vasuki.db")
