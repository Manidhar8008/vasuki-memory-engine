import sqlite3

conn=sqlite3.connect("vasuki.db")
cur=conn.cursor()

rows=cur.execute("""
SELECT evidence_type,COUNT(*)
FROM founder_evidence
GROUP BY evidence_type
ORDER BY COUNT(*) DESC
""").fetchall()

for etype,count in rows:

    obs=f"Activity detected around {etype}: {count} signals"

    cur.execute("""
    INSERT INTO founder_observations(
        observation,
        confidence
    )
    VALUES(?,?)
    """,(
        obs,
        min(1.0,count/100)
    ))

conn.commit()

print("OBSERVATIONS BUILT")

conn.close()
