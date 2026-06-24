CR	EATE TABLE IF NOT EXISTS goals(
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    status TEXT,
    priority INTEGER,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS decisions(
    id INTEGER PRIMARY KEY,
    decision TEXT,
    reason TEXT,
    impact TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS learnings(
    id INTEGER PRIMARY KEY,
    learning TEXT,
    source TEXT,
    confidence REAL,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS failures(
    id INTEGER PRIMARY KEY,
    failure TEXT,
    lesson TEXT,
    severity INTEGER,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS projects(
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    status TEXT,
    progress INTEGER,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS people(
    id INTEGER PRIMARY KEY,
    name TEXT,
    relationship TEXT,
    notes TEXT,
    created_at TEXT
);
