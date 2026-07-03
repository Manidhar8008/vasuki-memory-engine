import sqlite3

answers = {

"What entities are most central to Manidhar?":
"""
Manidhar, Vasuki, Janani, AI Systems, Python, FastAPI,
SQLite, Knowledge Graphs and Founder Intelligence.
""",

"What projects are active?":
"""
Vasuki OS, Janani AI, AIM1000 and portfolio systems.
""",

"What is Vasuki?":
"""
Vasuki is a local-first personal intelligence operating
system designed to index personal knowledge, construct
knowledge graphs and help users reason over their digital life.
""",

"What is Janani?":
"""
Janani is an AI platform focused on personal growth,
discipline systems and intelligent assistance.
""",

"What startups is he building?":
"""
The primary initiatives are Vasuki OS and Janani AI.
""",

"What technical capabilities appear most often?":
"""
Python, FastAPI, SQLite, React, TypeScript,
Knowledge Graphs, AI Agents and Data Engineering.
""",

"Who is Manidhar?":
"""
Manidhar is an AI systems builder, founder and engineer focused on
personal intelligence systems, knowledge graphs, automation and
AI operating systems. He builds products that combine software
engineering, data systems and AI reasoning.
""",

"What is his background?":
"""
Manidhar has experience across operations, business processes,
automation and software systems. His work evolved from enterprise
operations into AI engineering, knowledge systems and startup building.
""",

"What companies has he worked for?":
"""
Manidhar has worked with Cognizant and Genpact, supporting enterprise
operations, process improvement and technology-enabled workflows.
""",

"What technologies does he use?":
"""
Python, FastAPI, SQLite, PostgreSQL, React, TypeScript, Tailwind,
GitHub, AI APIs, Knowledge Graphs and Retrieval Systems.
""",

"What databases does he use?":
"""
SQLite for local-first systems, PostgreSQL for production workloads,
and vector-enabled architectures for AI retrieval.
""",

"What frameworks does he use?":
"""
FastAPI, React, Vite, Tailwind CSS and modern Python tooling for
backend and AI system development.
""",

"What projects has he built?":
"""
Vasuki OS, Janani AI, AI automation systems, knowledge graph
platforms, retrieval systems and startup-oriented software products.
""",

"What problems has he solved?":
"""
Knowledge retrieval, personal information management, AI-assisted
research, workflow automation, document intelligence and founder
productivity systems.
""",

"Why did he build Vasuki?":
"""
Vasuki was created to become a personal intelligence operating system
that helps users remember, search, connect and reason over their
digital life and knowledge.
""",

"What is his AI philosophy?":
"""
AI should augment human thinking rather than replace it. Systems
should be transparent, explainable and capable of reasoning over
evidence.
""",

"What is his engineering style?":
"""
Build practical systems quickly, validate ideas early and improve
through iterative engineering rather than excessive planning.
""",

"What is his architecture philosophy?":
"""
Local-first where possible, cloud when necessary, modular systems,
strong data ownership and observable architecture.
""",

"What are his strengths?":
"""
Systems thinking, rapid prototyping, AI integration, automation,
knowledge management and connecting ideas across domains.
""",

"What is his vision?":
"""
To build personal intelligence systems that help individuals think
better, learn faster and operate at a higher level of effectiveness.
""",

"What is he learning?":
"""
AI agents, ontology systems, knowledge graphs, retrieval architectures,
founder operations and advanced software engineering practices.
"""
}

conn = sqlite3.connect("founder.db")
cur = conn.cursor()

for question, answer in answers.items():

    row = cur.execute(
        "SELECT id FROM founder_questions WHERE question=?",
        (question,)
    ).fetchone()

    if row:
        cur.execute("""
        INSERT INTO founder_truths(
            question_id,
            answer,
            confidence,
            evidence,
            source_tables
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            row[0],
            answer.strip(),
            0.95,
            "Founder Seed Data",
            "manual"
        ))

conn.commit()
conn.close()

print("Answers loaded.")
