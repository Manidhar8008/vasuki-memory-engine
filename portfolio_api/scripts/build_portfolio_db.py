import sqlite3

SOURCE_DB="/data/data/com.termux/files/home/vasuki/vasuki.db"
TARGET_DB="/data/data/com.termux/files/home/vasuki/portfolio_api/data/portfolio.db"

source=sqlite3.connect(SOURCE_DB)
target=sqlite3.connect(TARGET_DB)

s=source.cursor()
t=target.cursor()

t.execute("DROP TABLE IF EXISTS stats")

t.execute("""
CREATE TABLE stats(
    metric TEXT PRIMARY KEY,
    value INTEGER
)
""")

stats = {
    "files": s.execute("SELECT COUNT(*) FROM files").fetchone()[0],
    "entities": s.execute("SELECT COUNT(*) FROM entities").fetchone()[0],
    "relationships": s.execute("SELECT COUNT(*) FROM relationships").fetchone()[0],
    "timeline": s.execute("SELECT COUNT(*) FROM timeline").fetchone()[0],
    "memories": s.execute("SELECT COUNT(*) FROM memories").fetchone()[0],
}

for k,v in stats.items():
    t.execute(
        "INSERT INTO stats(metric,value) VALUES(?,?)",
        (k,v)
    )

target.commit()

print(stats)
