import sqlite3

DB = "vasuki.db"


def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def rebuild_patterns():

    conn = get_conn()

    conn.execute("DELETE FROM founder_patterns")

    tech_keywords = [
        "Python",
        "FastAPI",
        "SQLite",
        "PostgreSQL",
        "React",
        "TypeScript",
        "Docker",
        "Git",
        "Qdrant",
        "Ollama"
    ]

    project_keywords = [
        "Vasuki",
        "Janani",
        "AIM1000",
        "Portfolio"
    ]

    docs = conn.execute("""
        SELECT content
        FROM documents
        LIMIT 1000
    """).fetchall()

    corpus = "\n".join([
        d["content"][:5000]
        for d in docs
        if d["content"]
    ])

    for tech in tech_keywords:
        count = corpus.lower().count(
            tech.lower()
        )

        if count > 0:
            conn.execute("""
                INSERT INTO founder_patterns
                (pattern_type, pattern_name)
                VALUES (?,?)
            """, (
                "technology",
                tech
            ))

    for project in project_keywords:
        count = corpus.lower().count(
            project.lower()
        )

        if count > 0:
            conn.execute("""
                INSERT INTO founder_patterns
                (pattern_type, pattern_name)
                VALUES (?,?)
            """, (
                "project",
                project
            ))

    conn.commit()
    conn.close()

    print("patterns refreshed")

def rebuild_insights():

    conn = get_conn()

    conn.execute(
        "DELETE FROM founder_insights"
    )

    doc_count = conn.execute(
        "SELECT COUNT(*) FROM documents"
    ).fetchone()[0]

    memory_count = conn.execute(
        "SELECT COUNT(*) FROM memories"
    ).fetchone()[0]

    conn.execute("""
        INSERT INTO founder_insights
        (
            insight_type,
            title,
            content,
            confidence,
            source_count
        )
        VALUES (?,?,?,?,?)
    """, (
        "identity",
        "Founder Profile",
        f"""
Manidhar appears to be an AI Systems Builder.

Knowledge base contains:

{doc_count} documents
{memory_count} memories

Primary focus appears to be
AI Systems,
Knowledge Graphs,
Personal Intelligence Infrastructure.
        """,
        0.90,
        doc_count
    ))

    conn.commit()
    conn.close()

    print("insights refreshed")

def rebuild_observations():

    conn = get_conn()

    conn.execute(
        "DELETE FROM founder_observations"
    )

    tables = [
        "documents",
        "memories",
        "concepts",
        "entities"
    ]

    for table in tables:

        try:

            count = conn.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

            conn.execute("""
                INSERT INTO founder_observations
                (
                    observation,
                    confidence
                )
                VALUES (?,?)
            """, (
                f"Activity detected around {table}: {count} records",
                1.0
            ))

        except:
            pass

    conn.commit()
    conn.close()

    print("observations refreshed")

if __name__ == "__main__":

    print("Founder Worker")

    rebuild_patterns()
    rebuild_insights()
    rebuild_observations()

    print("Done")
