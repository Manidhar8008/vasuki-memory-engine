#!/usr/bin/env python3
from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Iterable

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "founder" / "founder.db"

# What we will ingest as readable content
TEXT_EXTS = {
    ".txt", ".md", ".py", ".json", ".yaml", ".yml", ".csv",
    ".log", ".html", ".htm", ".xml", ".toml", ".ini", ".cfg",
    ".sql", ".sh", ".css", ".js", ".ts", ".tsx", ".jsx"
}

# What we skip entirely
SKIP_DIRS = {
    "venv", ".venv", "__pycache__", ".git", ".idea", ".mypy_cache",
    ".pytest_cache", "node_modules", "dist", "build", ".next",
}

def connect() -> sqlite3.Connection:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def ensure_tables(conn: sqlite3.Connection) -> None:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS founder_artifacts(
        id INTEGER PRIMARY KEY,
        path TEXT,
        filename TEXT,
        filetype TEXT,
        size INTEGER,
        created_at TEXT,
        category TEXT,
        processed INTEGER DEFAULT 0
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS founder_content(
        id INTEGER PRIMARY KEY,
        filename TEXT,
        content TEXT
    )
    """)
    conn.commit()

def already_has_artifact(conn: sqlite3.Connection, path: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM founder_artifacts WHERE path=? LIMIT 1",
        (path,)
    ).fetchone()
    return row is not None

def already_has_content(conn: sqlite3.Connection, filename: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM founder_content WHERE filename=? LIMIT 1",
        (filename,)
    ).fetchone()
    return row is not None

def read_sample_files() -> list[Path]:
    candidates = [
        BASE_DIR / "sample_files.txt",
        BASE_DIR / "founder" / "sample_files.txt",
    ]
    for fp in candidates:
        if fp.exists():
            items = []
            for line in fp.read_text(errors="ignore").splitlines():
                line = line.strip()
                if line and os.path.exists(line):
                    items.append(Path(line))
            if items:
                return items
    return []

def walk_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        parts = set(Path(dirpath).parts)
        if parts & SKIP_DIRS:
            dirnames[:] = []
            continue

        # prune bad dirs in-place
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for name in filenames:
            p = Path(dirpath) / name

            if p.name in {"founder.db", "vasuki.db", "vasuki_backup.db"}:
                continue
            if ".git" in p.parts or "venv" in p.parts or ".venv" in p.parts:
                continue

            yield p

def should_store_content(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTS and path.is_file()

def safe_read_text(path: Path) -> str | None:
    try:
        return path.read_text(errors="ignore")
    except Exception:
        return None

def ingest_paths(conn: sqlite3.Connection, paths: Iterable[Path]) -> tuple[int, int]:
    artifact_inserts = 0
    content_inserts = 0

    for p in paths:
        try:
            if not p.exists() or not p.is_file():
                continue

            abs_path = str(p.resolve())
            filename = p.name
            filetype = p.suffix.lower()
            size = p.stat().st_size

            if not already_has_artifact(conn, abs_path):
                conn.execute(
                    """
                    INSERT INTO founder_artifacts(
                        path, filename, filetype, size, created_at, category, processed
                    )
                    VALUES (?, ?, ?, ?, datetime('now'), NULL, 0)
                    """,
                    (abs_path, filename, filetype, size),
                )
                artifact_inserts += 1

            if should_store_content(p) and not already_has_content(conn, filename):
                text = safe_read_text(p)
                if text is not None and text.strip():
                    conn.execute(
                        """
                        INSERT INTO founder_content(filename, content)
                        VALUES (?, ?)
                        """,
                        (filename, text),
                    )
                    content_inserts += 1

        except Exception as e:
            print(f"[skip] {p}: {e}")

    conn.commit()
    return artifact_inserts, content_inserts

def main() -> None:
    print(f"[db] {DB_PATH}")
    with connect() as conn:
        ensure_tables(conn)

        sample_files = read_sample_files()
        if sample_files:
            print(f"[scan] sample_files.txt -> {len(sample_files)} files")
            arts, cont = ingest_paths(conn, sample_files)
        else:
            root = BASE_DIR
            print(f"[scan] recursive walk -> {root}")
            arts, cont = ingest_paths(conn, walk_files(root))

        counts = {
            "founder_artifacts": conn.execute("SELECT COUNT(*) FROM founder_artifacts").fetchone()[0],
            "founder_content": conn.execute("SELECT COUNT(*) FROM founder_content").fetchone()[0],
        }

    print(f"[done] inserted artifacts={arts}, content={cont}")
    print(f"[counts] {counts}")

if __name__ == "__main__":
    main()
