CREATE TABLE IF NOT EXISTS identity_facts(
    id INTEGER PRIMARY KEY,
    category TEXT,
    fact TEXT,
    confidence REAL,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS life_principles(
    id INTEGER PRIMARY KEY,
    principle TEXT,
    source TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS legacy_items(
    id INTEGER PRIMARY KEY,
    category TEXT,
    content TEXT,
    created_at TEXT
);
