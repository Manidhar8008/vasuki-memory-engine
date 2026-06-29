import sqlite3
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

DB_PATH = "vasuki.db"

class VasukiMetaAgent:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        if not Path(db_path).exists():
            raise FileNotFoundError(f"Database not found: {db_path}")
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        self.conn.close()

    # --- Core utilities ---
    def table_exists(self, table_name: str) -> bool:
        cur = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        return cur.fetchone() is not None

    def columns(self, table_name: str) -> list[str]:
        if not self.table_exists(table_name):
            return []
        cur = self.conn.execute(f"PRAGMA table_info({table_name})")
        return [row["name"] for row in cur.fetchall()]

    def rows(self, table_name: str) -> list[sqlite3.Row]:
        if not self.table_exists(table_name):
            return []
        cur = self.conn.execute(f"SELECT * FROM {table_name}")
        return cur.fetchall()

    def parse_tags(self, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, (list, tuple)):
            return [str(x).strip().lower() for x in value if str(x).strip()]
        text = str(value).strip()
        if not text:
            return []
        if text.startswith("[") and text.endswith("]"):
            try:
                data = json.loads(text)
                if isinstance(data, list):
                    return [str(x).strip().lower() for x in data if str(x).strip()]
            except Exception:
                pass
        parts = re.split(r"[,\|;#/]+", text)
        return [p.strip().lower() for p in parts if p.strip()]

    def safe_int(self, value: Any) -> int:
        try:
            return int(value)
        except Exception:
            return 0

    def print_header(self, title: str):
        print("\n" + "=" * 72)
        print(title)
        print("=" * 72)

    # --- Reports ---
    def capability_report(self) -> str:
        docs = self.rows("documents")
        events = self.rows("events")
        files = self.rows("files")

        documents_cols = set(self.columns("documents"))
        events_cols = set(self.columns("events"))

        capabilities = {
            "pdf_ingestion": len(docs) > 0,
            "memory_storage": self.table_exists("events") or self.table_exists("documents"),
            "search_ready": len(docs) > 0 or len(events) > 0,
            "tag_analytics": ("tags" in documents_cols) or ("tags" in events_cols),
            "source_tracking": ("source" in documents_cols) or ("source" in events_cols),
            "time_tracking": any(
                c in documents_cols or c in events_cols
                for c in ["created_at", "modified_at", "timestamp"]
            ),
            "content_index": ("content" in documents_cols) or ("content" in events_cols),
            "file_registry": len(files) > 0 or self.table_exists("files"),
        }

        lines = ["VASUKI CAPABILITY REPORT"]
        for k, v in capabilities.items():
            lines.append(f"- {k}: {'READY' if v else 'NOT READY'}")

        lines.append(f"- documents_rows: {len(docs)}")
        lines.append(f"- events_rows: {len(events)}")
        lines.append(f"- files_rows: {len(files)}")
        return "\n".join(lines)

    def metadata_insights(self):
        self.print_header("VASUKI METADATA INSIGHTS")

        # Table overview
        tables = [t for t in ["documents", "events", "files"] if self.table_exists(t)]
        print("Tables:", ", ".join(tables) if tables else "none")

        # Documents table analysis
        if self.table_exists("documents"):
            docs = self.rows("documents")
            cols = self.columns("documents")
            print("\n[documents]")
            print("columns:", ", ".join(cols))
            print(f"rows: {len(docs)}")

            # Coverage checks
            if "title" in cols:
                title_count = sum(1 for r in docs if str(r["title"] or "").strip())
                print(f"title_coverage: {title_count}/{len(docs)}")

            if "tags" in cols:
                tag_counter = Counter()
                for r in docs:
                    tag_counter.update(self.parse_tags(r["tags"]))
                print("top_tags:", dict(tag_counter.most_common(10)))

        # Events table analysis
        if self.table_exists("events"):
            events = self.rows("events")
            cols = self.columns("events")
            print("\n[events]")
            print("columns:", ", ".join(cols))
            print(f"rows: {len(events)}")

        # Files table analysis
        if self.table_exists("files"):
            files = self.rows("files")
            cols = self.columns("files")
            print("\n[files]")
            print("columns:", ", ".join(cols))
            print(f"rows: {len(files)}")

        self.print_header("CAPABILITY STATUS")
        print(self.capability_report())

    # --- Search ---
    def search(self, query: str):
        query = query.strip()
        if not query:
            print("Empty query.")
            return

        print("\nSEARCH RESULTS")
        found = False

        if self.table_exists("documents"):
            rows = self.conn.execute(
                """
                SELECT title, path, chars
                FROM documents
                WHERE content LIKE ? OR title LIKE ? OR path LIKE ?
                LIMIT 20
                """,
                (f"%{query}%", f"%{query}%", f"%{query}%")
            ).fetchall()
            if rows:
                found = True
                print("\n[documents]")
                for r in rows:
                    print(f"- {r['title']} | chars={r['chars']} | {r['path']}")

        if self.table_exists("events"):
            rows = self.conn.execute(
                """
                SELECT title, source, type
                FROM events
                WHERE content LIKE ? OR title LIKE ? OR tags LIKE ?
                LIMIT 20
                """,
                (f"%{query}%", f"%{query}%", f"%{query}%")
            ).fetchall()
            if rows:
                found = True
                print("\n[events]")
                for r in rows:
                    print(f"- {r['title']} | {r['source']} | {r['type']}")

        if not found:
            print("No matches found.")

    # --- CLI loop ---
    def run(self):
        self.metadata_insights()
        while True:
            try:
                q = input("\nVasuki> ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nBye.")
                break

            if not q:
                continue

            low = q.lower()
            if low in {"exit", "quit", "q"}:
                print("Bye.")
                break
            elif low in {"capabilities", "status", "report"}:
                print("\n" + self.capability_report())
            elif low in {"insights", "meta", "metadata"}:
                self.metadata_insights()
            elif low.startswith("search "):
                self.search(q[7:])
            else:
                self.search(q)

if __name__ == "__main__":
    agent = VasukiMetaAgent()
    try:
        agent.run()
    finally:
        agent.close()
