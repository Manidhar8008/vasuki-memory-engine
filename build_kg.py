import sqlite3

DB_PATH = "vasuki.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

print("Building Vasuki Knowledge Graph...")

# ----------------------------------
# STEP 1: Import entities as nodes
# ----------------------------------

entities = conn.execute("""
    SELECT entity, entity_type
    FROM entities
    LIMIT 5000
""").fetchall()

node_count = 0

for row in entities:

    entity = row["entity"]
    entity_type = row["entity_type"]

    existing = conn.execute("""
        SELECT id
        FROM kg_nodes
        WHERE node_name = ?
    """, (entity,)).fetchone()

    if existing:
        continue

    conn.execute("""
        INSERT INTO kg_nodes (
            node_type,
            node_name,
            metadata
        )
        VALUES (?, ?, ?)
    """, (
        entity_type.upper(),
        entity,
        "auto-generated"
    ))

    node_count += 1

# ----------------------------------
# STEP 2: Import relationships
# ----------------------------------

rels = conn.execute("""
    SELECT
        concept_a,
        concept_b,
        weight
    FROM relationships
""").fetchall()

edge_count = 0

for row in rels:

    conn.execute("""
        INSERT INTO kg_edges (
            source_node,
            target_node,
            relation,
            weight
        )
        VALUES (?, ?, ?, ?)
    """, (
        row["concept_a"],
        row["concept_b"],
        "RELATED_TO",
        row["weight"]
    ))

    edge_count += 1

conn.commit()

print(f"Added {node_count} nodes")
print(f"Added {edge_count} edges")

print("Done.")

conn.close()
