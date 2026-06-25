from pathlib import Path
import sqlite3

DB_DIR = Path("memory")
DB_DIR.mkdir(exist_ok=True)

DB_FILE = DB_DIR / "founder.db"


class Database:

    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row
        self.initialize()

    def initialize(self):

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS memories(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT NOT NULL,

            type TEXT NOT NULL,

            content TEXT NOT NULL,

            source TEXT,

            device TEXT,

            tags TEXT
        )
        """)

        self.conn.commit()

    def execute(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        return cur

    def query(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

    def close(self):
        self.conn.close()


db = Database()


if __name__ == "__main__":
    print("✓ Database initialized successfully.")
