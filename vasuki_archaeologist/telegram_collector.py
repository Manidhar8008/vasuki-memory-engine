import sqlite3
import json
from pathlib import Path

DB = "../vasuki.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS telegram_messages (
id INTEGER PRIMARY KEY AUTOINCREMENT,
chat_name TEXT,
sender TEXT,
timestamp TEXT,
message TEXT
)
""")

EXPORT_FOLDER = "./telegram_exports"

for file in Path(EXPORT_FOLDER).glob("*.json"):

print(f"Processing {file}")

with open(file, "r", encoding="utf-8") as f:

    data = json.load(f)

    chat_name = data.get("name", "unknown")

    for msg in data.get("messages", []):

        sender = msg.get("from", "unknown")
        timestamp = msg.get("date", "")

        text = msg.get("text", "")

        if isinstance(text, list):

            parts = []

            for item in text:

                if isinstance(item, str):
                    parts.append(item)

                elif isinstance(item, dict):
                    parts.append(
                        item.get("text", "")
                    )

            text = " ".join(parts)

        cur.execute("""
        INSERT INTO telegram_messages(
            chat_name,
            sender,
            timestamp,
            message
        )
        VALUES (?,?,?,?)
        """,
        (
            chat_name,
            sender,
            timestamp,
            text
        ))

conn.commit()
conn.close()

print("Telegram Import Complete")
