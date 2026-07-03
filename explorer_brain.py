import sqlite3

DB = "vasuki.db"


def get_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def get_technologies():

    conn = get_connection()

    rows = conn.execute("""
    SELECT pattern_name
    FROM founder_patterns
    WHERE pattern_type='technology'
    ORDER BY pattern_name
    """).fetchall()

    conn.close()

    return [r["pattern_name"] for r in rows]


def get_projects():

    conn = get_connection()

    rows = conn.execute("""
    SELECT pattern_name
    FROM founder_patterns
    WHERE pattern_type='project'
    ORDER BY pattern_name
    """).fetchall()

    conn.close()

    return [r["pattern_name"] for r in rows]


def get_states():

    conn = get_connection()

    rows = conn.execute("""
    SELECT state_name, score
    FROM founder_state
    ORDER BY score DESC
    """).fetchall()

    conn.close()

    return rows


def recruiter_summary():

    projects = get_projects()
    techs = get_technologies()

    return f"""
👤 Founder Profile

Manidhar is an AI Systems Builder focused on Personal Intelligence Systems, Knowledge Graphs and AI-powered products.

🚀 Projects

• {'\n• '.join(projects)}

⚙️ Technologies

• {'\n• '.join(techs)}

🎯 Current Focus

• AI Systems
• Knowledge Management
• Automation
• Software Engineering
""".strip()


def answer(query):

    q = query.lower().strip()

    if "who" in q and "manidhar" in q:
    return {
        "type":"founder",
        "answer":"""
Manidhar is an AI Systems Engineer focused on knowledge systems, retrieval architectures, local-first AI, and automation.

Core projects:
• Vasuki
• Janani

Primary technologies:
• Python
• FastAPI
• SQLite

Current focus:
• Personal Intelligence Systems
• Knowledge Retrieval
• AI Infrastructure
"""
    }

    if "forward deployed" in q or "fde" in q:
    return {
        "type":"fde",
        "answer":"""
Manidhar demonstrates Forward Deployed Engineering characteristics:

• Builds directly from real-world problems.
• Owns product, architecture, and implementation.
• Works across frontend, backend, databases, and AI systems.
• Converts unstructured data into operational systems.
• Rapidly prototypes and ships independently.

Projects such as Vasuki required system design, data engineering, knowledge modeling, retrieval systems, and user-facing product development.
"""
    }

    if any(k in q for k in [
        "technology",
        "technologies",
        "tech",
        "stack",
        "skills"
    ]):

        return {
            "type": "technology",
            "answer": ", ".join(get_technologies())
        }

    if any(k in q for k in [
        "project",
        "projects",
        "built",
        "building",
        "startup",
        "startups"
    ]):

        return {
            "type": "project",
            "answer": ", ".join(get_projects())
        }

    if "focus" in q:

        states = get_states()

        return {
            "type": "focus",
            "answer": " | ".join(
                f"{r['state_name']} ({round(r['score'],1)})"
                for r in states[:5]
            )
        }

    if "who" in q or "manidhar" in q:

        return {
            "type": "profile",
            "answer": recruiter_summary()
        }

    return {
        "type": "profile",
        "answer": recruiter_summary()
    }
