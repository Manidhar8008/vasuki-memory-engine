import sqlite3

# Intent-optimized foundational truths
FOUNDER_TRUTHS = {
    "vasuki": """
Vasuki is a local-first personal intelligence operating system.              
Core Components:
• File Indexing
• Knowledge Graph
• Timeline Engine
• Memory System
• Retrieval Layer
• Multi-Agent Architecture

Tech Stack:
Python | FastAPI | SQLite | React | TypeScript | Qdrant | Ollama
""",
    "manidhar": """
Manidhar Pati is an AI Systems Engineer and Founder.                         
He builds:
• Vasuki AI
• Knowledge Engines
• Personal Intelligence Systems
• Retrieval Systems
• Agent Architectures

Focus Areas:
AI Infrastructure | Local-first Systems | RAG | Automation | Knowledge Management
""",
    "hire manidhar": """
Built a functioning personal intelligence platform from scratch.

Experience:
• FastAPI | React | SQLite
• AI Agents | Knowledge Graphs | Retrieval Systems

Strength:
Designing complete AI products end-to-end.
"""
}

DB = "vasuki.db"

def get_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def search_founder_patterns(query):
    conn = get_connection()
    rows = conn.execute("""
        SELECT pattern_name, pattern_type
        FROM founder_patterns
        WHERE lower(pattern_name) LIKE ?
    """, (f"%{query.lower()}%",)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def search_memories(query, limit=5):
    conn = get_connection()
    try:
        rows = conn.execute("""
            SELECT memory, confidence
            FROM memories
            WHERE rowid IN (
                SELECT rowid
                FROM memory_fts
                WHERE memory_fts MATCH ?
            )
            LIMIT ?
        """, (query, limit)).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        conn.close()
        return []


def search_documents(query, limit=3):
    conn = get_connection()
    try:
        rows = conn.execute("""
            SELECT title, substr(content,1,1000) as content
            FROM documents
            WHERE rowid IN (
                SELECT rowid
                FROM document_fts
                WHERE document_fts MATCH ?
            )
            LIMIT ?
        """, (query, limit)).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        conn.close()
        return []


def search_concepts(query, limit=5):
    conn = get_connection()
    try:
        rows = conn.execute("""
            SELECT concept_name
            FROM concepts
            WHERE lower(concept_name) LIKE ?
            LIMIT ?
        """, (f"%{query.lower()}%", limit)).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        conn.close()
        return []


def search_period(period):
    conn = get_connection()
    try:
        rows = conn.execute("""
            SELECT *
            FROM founder_periods
            WHERE period = ?
        """, (period,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        conn.close()
        return []


def search_screenshots(query):
    conn = get_connection()
    try:
        rows = conn.execute("""
            SELECT raw_text 
            FROM ocr_records 
            WHERE lower(raw_text) LIKE ?
        """, (f"%{query.lower()}%",)).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        conn.close()
        return []


def answer(query):
    # Inbound telemetry
    print(f"[QUERY] {query}")
    
    # Normalize input and strip common trailing punctuation
    q = query.lower().strip().rstrip('?.')

    # 1. Direct Card Phrase Intercepts (Guarantees exact UI triggers)
    if q == "show flagship projects":
        print("[ROUTE] direct_card_flagship")
        return {
            "type": "truth",
            "answer": "Flagship Systems\n\n1. Vasuki AI\n   Personal Intelligence Platform\n\n2. Janani AI\n   Discipline Engine\n\n3. AIM1000\n   Job Automation System\n\n4. Startup Broadcasting System\n   Content Automation Platform"
        }

    if q == "explain vasuki architecture":
        print("[ROUTE] direct_card_architecture")
        return {
            "type": "truth",
            "answer": "Vasuki Architecture\n\nFrontend:\nReact + TypeScript\n\nAPI:\nFastAPI\n\nDatabase:\nSQLite\n\nKnowledge:\nGraph + Timeline + Memory\n\nFuture:\nVector Search + Multi-Agent Layer"
        }

    if q == "what business problems were solved":
        print("[ROUTE] direct_card_business")
        return {
            "type": "truth",
            "answer": "Business Problems Solved\n\n• Knowledge retrieval\n• Personal memory search\n• Information organization\n• AI workflow automation\n• Founder operating systems\n• Content generation systems"
        }

    if q == "why hire manidhar":
        print("[ROUTE] direct_card_hire")
        return {
            "type": "truth",
            "source": "founder_truths",
            "answer": FOUNDER_TRUTHS["hire manidhar"]
        }

    # 2. Token-Based Intent Matching (Founder Truths)
    for key, value in FOUNDER_TRUTHS.items():
        words = key.split()
        if all(word in q for word in words):
            print(f"[ROUTE] founder_truth ({key})")
            return {
                "type": "truth",
                "source": "founder_truths",
                "answer": value
            }

    # 3. Dedicated Intent Blocks
    if "flagship" in q:
        print("[ROUTE] intent_flagship")
        return {
            "type": "truth",
            "answer": "Flagship Systems\n\n1. Vasuki AI\n2. Janani AI\n3. AIM1000\n4. Startup Broadcasting System"
        }

    if "project" in q:
        print("[ROUTE] intent_projects")
        return {
            "type": "truth",
            "answer": "Projects Ecosystem\n\n• Vasuki AI: Personal Operating System\n• JAN.AI: Multi-platform media manager\n• mw.ai: Data Services portfolio\n• AI Trading OS: Market Scanner & Journaling engine"
        }

    if "architecture" in q or "stack" in q:
        print("[ROUTE] intent_architecture")
        return {
            "type": "truth",
            "answer": "Vasuki Architecture\n\nFrontend: React + TypeScript\nAPI: FastAPI\nDatabase: SQLite\nKnowledge Strategy: Graph + Timeline + Memory"
        }

    if "business" in q or "problem" in q:
        print("[ROUTE] intent_business")
        return {
            "type": "truth",
            "answer": "Business Focus\n\n• Workflow automation\n• Local knowledge graph discovery\n• Structural data indexing systems"
        }

    if "skills" in q or "technology" in q or "tech stack" in q:
        print("[ROUTE] intent_skills")
        return {
            "type": "truth",
            "answer": "Core Technologies\n\nFrontend:\nReact\nTypeScript\nTailwind\n\nBackend:\nPython\nFastAPI\n\nData:\nSQLite\nPostgreSQL\n\nAI:\nRAG\nAgents\nKnowledge Graphs\nVector Search"
        }

    # 4. Timeline Lookup (Years)
    for year in ["2022", "2023", "2024", "2025", "2026"]:
        if year in query:
            periods = search_period(year)
            if periods:
                p = periods[0]
                print(f"[ROUTE] timeline_period ({year})")
                return {
                    "type": "period",
                    "source": "founder_periods",
                    "answer": f"Period: {p['period']}\n\nTopics:\n{p['dominant_topics']}\n\nProjects:\n{p['top_projects']}\n\nSummary:\n{p['summary']}\n\nEvidence Count:\n{p['evidence_count']}"
                }

    # 5. Fallback Dynamic Database Searches
    memories = search_memories(query)
    if memories:
        print("[ROUTE] dynamic_memories")
        return {
            "type": "memory",
            "source": "memories",
            "answer": "\n\n".join([m["memory"] for m in memories])
        }

    docs = search_documents(query)
    if docs and len(query.split()) >= 2:
        text = [f"{d['title']}\n\n{d['content']}" for d in docs]
        print("[ROUTE] dynamic_documents")
        return {
            "type": "document",
            "source": "documents",
            "answer": "\n\n---\n\n".join(text)
        }

    shots = search_screenshots(query)
    if shots:
        print("[ROUTE] dynamic_screenshots")
        return {
            "type": "screenshots",
            "source": "ocr_records",
            "answer": "\n\n".join([s["raw_text"][:500] for s in shots])
        }

    # 6. Final Catch-All
    print("[ROUTE] fallback_not_found")
    return {
        "type": "not_found",
        "answer": "No relevant information found."
    }

