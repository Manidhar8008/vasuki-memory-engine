import sqlite3

DB = "../vasuki.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

RULES = {

"vasuki": [

    ("RELATED_TO","Memory System"),
    ("RELATED_TO","Agent"),
    ("RELATED_TO","SQLite"),
    ("RELATED_TO","Termux")

],

"mw.ai": [

    ("RELATED_TO","CRM"),
    ("RELATED_TO","Tier 2 Cities"),
    ("RELATED_TO","Data Systems")

],

"janani": [

    ("RELATED_TO","Personal AI"),
    ("RELATED_TO","Vasuki")

]

}

cur.execute("""
SELECT id,message
FROM telegram_messages
""")

for row in cur.fetchall():

msg_id = row[0]
text = str(row[1]).lower()

for entity in RULES:

    if entity in text:

        for relation,target in RULES[entity]:

            cur.execute("""
            SELECT COUNT(*)
            FROM entity_relationships
            WHERE entity_a=?
            AND relationship=?
            AND entity_b=?
            """,
            (
                entity,
                relation,
                target
            ))

            exists = cur.fetchone()[0]

            if exists == 0:

                cur.execute("""
                INSERT INTO entity_relationships(
                    entity_a,
                    relationship,
                    entity_b,
                    artifact_id,
                    confidence
                )
                VALUES(?,?,?,?,?)
                """,
                (
                    entity,
                    relation,
                    target,
                    msg_id,
                    0.9
                ))

conn.commit()
conn.close()

print("Relationships Added")
