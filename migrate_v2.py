import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

# ARTIFACTS

cur.execute("""
CREATE TABLE IF NOT EXISTS artifacts_v2(
    id INTEGER PRIMARY KEY,

    artifact_type TEXT,
    title TEXT,

    path TEXT UNIQUE,

    content TEXT,

    chars INTEGER,

    file_size INTEGER,

    created_at TEXT,
    modified_at TEXT,

    source TEXT,

    tags TEXT
)
""")

# MEMORIES

cur.execute("""
CREATE TABLE IF NOT EXISTS memories(
    id INTEGER PRIMARY KEY,

    artifact_id INTEGER,

    memory_type TEXT,

    memory TEXT,

    confidence REAL,

    created_at TEXT
)
""")

# ENTITIES

cur.execute("""
CREATE TABLE IF NOT EXISTS entities(
    id INTEGER PRIMARY KEY,

    name TEXT,

    entity_type TEXT,

    frequency INTEGER DEFAULT 1,

    created_at TEXT
)
""")

# RELATIONSHIPS

cur.execute("""
CREATE TABLE IF NOT EXISTS relationships(
    id INTEGER PRIMARY KEY,

    source_entity INTEGER,

    relation TEXT,

    target_entity INTEGER,

    confidence REAL
)
""")

# OBSERVATIONS

cur.execute("""
CREATE TABLE IF NOT EXISTS observations(
    id INTEGER PRIMARY KEY,

    artifact_id INTEGER,

    observation TEXT,

    category TEXT,

    confidence REAL
)
""")

# TIMELINE

cur.execute("""
CREATE TABLE IF NOT EXISTS timeline(
    id INTEGER PRIMARY KEY,

    event_date TEXT,

    event_type TEXT,

    title TEXT,

    description TEXT,

    artifact_id INTEGER
)
""")

# FOUNDER STATE

cur.execute("""
CREATE TABLE IF NOT EXISTS founder_state(
    id INTEGER PRIMARY KEY,

    state_name TEXT,

    score REAL,

    evidence_count INTEGER,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

# INDEXES

cur.execute("""
CREATE INDEX IF NOT EXISTS idx_artifact_path
ON artifacts_v2(path)
""")

cur.execute("""
CREATE INDEX IF NOT EXISTS idx_entity_name
ON entities(name)
""")

cur.execute("""
CREATE INDEX IF NOT EXISTS idx_memory_type
ON memories(memory_type)
""")

conn.commit()

print("VASUKI V2 READY")

conn.close()
