#!/data/data/com.termux/files/usr/bin/bash

echo "Creating database.py..."

cat > database.py << 'EOF'
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
EOF

echo "Creating memory.py..."

cat > memory.py << 'EOF'
import json
from datetime import datetime
import sqlite3

DB = sqlite3.connect("memory/vasuki.db")
DB.row_factory = sqlite3.Row


def save_memory(content,
                memory_type="memory",
                source="terminal",
                device="builder-phone",
                tags=None):

    if tags is None:
        tags = []

    DB.execute(
        """
        INSERT INTO memories
        (
            timestamp,
            type,
            content,
            source,
            device,
            tags
        )
        VALUES
        (?,?,?,?,?,?)
        """,
        (
            datetime.now().isoformat(),
            memory_type,
            content,
            source,
            device,
            json.dumps(tags),
        ),
    )

    DB.commit()

    return "Memory Stored"


def recent(limit=5):

    rows = DB.execute(
        """
        SELECT *
        FROM memories
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    return [dict(x) for x in rows]


def search(query):

    rows = DB.execute(
        """
        SELECT *
        FROM memories
        WHERE content LIKE ?
        ORDER BY id DESC
        """,
        (f"%{query}%",),
    ).fetchall()

    return [dict(x) for x in rows]


if __name__ == "__main__":

    save_memory("Hello Vasuki")

    print(recent())
EOF

echo ""
echo "=============================="
echo " STEP 1 COMPLETE"
echo "=============================="
echo ""
echo "Run:"
echo "python database.py"
echo "python memory.py"
