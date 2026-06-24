CREATE TABLE IF NOT EXISTS activity_log(
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    source TEXT,
    activity_type TEXT,
    title TEXT,
    content TEXT,
    metadata TEXT
);

CREATE INDEX IF NOT EXISTS idx_activity_time
ON activity_log(timestamp);

CREATE INDEX IF NOT EXISTS idx_activity_source
ON activity_log(source);
