import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS canonical_entities(
id INTEGER PRIMARY KEY,
canonical_name TEXT,
alias TEXT
)
""")

MAP = {
    "janani":"JANANI",
    "janani.ai":"JANANI",
    "janani-ai":"JANANI",

    "vasuki":"VASUKI",
    "vasuki os":"VASUKI",
    "project vasuki":"VASUKI",

    "mw.ai":"MWAI",
    "mw_ai":"MWAI",
    "mwai":"MWAI"
}

for alias,canonical in MAP.items():

    cur.execute("""
    INSERT INTO canonical_entities(
    canonical_name,
    alias
    )
    VALUES(?,?)
    """,(canonical,alias))

conn.commit()

print("CANONICALS CREATED")

conn.close()
