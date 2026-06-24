import sqlite3

conn=sqlite3.connect("vasuki.db")
cur=conn.cursor()

rows=cur.execute("""
SELECT evidence_type,COUNT(*)
FROM founder_evidence
GROUP BY evidence_type
""").fetchall()

for state,count in rows:

    cur.execute("""
    INSERT INTO founder_state(
        state_name,
        score,
        evidence_count
    )
    VALUES(?,?,?)
    """,(
        state,
        round(count/10,2),
        count
    ))

conn.commit()

print("STATE MODEL BUILT")

conn.close()
