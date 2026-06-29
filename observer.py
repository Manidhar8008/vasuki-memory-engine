import sqlite3
from pathlib import Path
from datetime import datetime

DB = "vasuki.db"

ROOTS = [
    "/storage/emulated/0/Download",
    "/storage/emulated/0/Documents",
    "/storage/emulated/0/Pictures",
    "/storage/emulated/0/DCIM",
    "/storage/emulated/0/AI_BRAIN_SYSTEM"
]

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT UNIQUE,
    name TEXT,
    extension TEXT,
    size INTEGER,
    created_at TEXT,
    modified_at TEXT
)
""")

count = 0

for root in ROOTS:
    root_path = Path(root)

    if not root_path.exists():
        continue

    for f in root_path.rglob("*"):

        if not f.is_file():
            continue

        try:
            stat = f.stat()

            cur.execute("""
            INSERT OR IGNORE INTO files
            (
                path,
                name,
                extension,
                size,
                created_at,
                modified_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                str(f),
                f.name,
                f.suffix.lower(),
                stat.st_size,
                datetime.fromtimestamp(
                    stat.st_ctime
                ).isoformat(),
                datetime.fromtimestamp(
                    stat.st_mtime
                ).isoformat()
            ))

            count += 1

        except Exception:
            pass

conn.commit()

print(f"Indexed {count} files")

conn.close()
