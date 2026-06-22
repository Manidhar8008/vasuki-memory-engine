import sqlite3

DB = "../vasuki.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

RULES = {

    "vasuki": [

        ("USES", "SQLite"),
        ("USES", "Termux"),
        ("CONTAINS", "Memory System"),
        ("CONTAINS", "Archaeologist Agent"),
        ("CONTAINS", "Relationship Mapper"),
        ("CONTAINS", "Identity Reconstructor")

    ],

    "mw.ai": [

        ("TARGETS", "Tier 2 Cities"),
        ("OFFERS", "CRM"),
        ("OFFERS", "Data Systems"),
        ("OFFERS", "Intern Program")

    ],

    "janani": [

        ("TYPE", "Personal AI"),
        ("CONNECTED_TO", "Vasuki")

    ]
}

cur.execute("""
SELECT id,title,content
FROM documents
""")

for doc_id,title,content in cur.fetchall():

    if not content:
        continue

    text = content.lower()

    for entity in RULES:

        if entity in text:

            for rel,target in RULES[entity]:

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
                    rel,
                    target,
                    doc_id,
                    0.80
                ))

conn.commit()
conn.close()

print("Relationships Created")
