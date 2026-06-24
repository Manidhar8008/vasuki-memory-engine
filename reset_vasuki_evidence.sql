
DROP TABLE IF EXISTS founder_evidence;

CREATE TABLE founder_evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type TEXT,
    source_path TEXT,
    evidence_type TEXT,
    evidence_text TEXT,
    confidence REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS founder_observations;

CREATE TABLE founder_observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    observation TEXT,
    confidence REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS founder_state;

CREATE TABLE founder_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state_name TEXT,
    score REAL,
    evidence_count INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

