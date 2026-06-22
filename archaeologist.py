import sqlite3
import sys
from rich.console import Console
from rich.panel import Panel

console = Console()

DB = "vasuki.db"


def search_documents(cur, query):
    cur.execute("""
        SELECT title,path,content
        FROM documents
        WHERE lower(content) LIKE ?
        LIMIT 10
    """, (f"%{query.lower()}%",))

    return cur.fetchall()


def search_concepts(cur, query):
    cur.execute("""
        SELECT concept,frequency
        FROM concepts
        WHERE lower(concept) LIKE ?
        ORDER BY frequency DESC
        LIMIT 20
    """, (f"%{query.lower()}%",))

    return cur.fetchall()


def search_memories(cur, query):

    try:
        cur.execute("""
            SELECT *
            FROM memories
            LIMIT 20
        """)
        return cur.fetchall()

    except:
        return []


def main():

    if len(sys.argv) < 2:
        print("\nUsage:")
        print("python archaeologist.py fastapi")
        return

    query = sys.argv[1]

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    console.print(
        Panel.fit(
            f"Searching Vasuki for: [bold green]{query}[/bold green]"
        )
    )

    docs = search_documents(cur, query)

    concepts = search_concepts(cur, query)

    memories = search_memories(cur, query)

    console.print("\n[bold cyan]DOCUMENT MATCHES[/bold cyan]\n")

    for i, row in enumerate(docs, start=1):

        title = row[0]
        path = row[1]
        content = row[2] or ""

        idx = content.lower().find(query.lower())

        if idx == -1:
            idx = 0

        snippet = content[max(0, idx-150):idx+300]

        console.print(f"[yellow]{i}. {title}[/yellow]")
        console.print(path)
        console.print(snippet)
        console.print("-" * 60)

    console.print("\n[bold cyan]CONCEPT MATCHES[/bold cyan]\n")

    for concept, freq in concepts:
        console.print(
            f"{concept} (frequency={freq})"
        )

    console.print("\n[bold cyan]MEMORY COUNT[/bold cyan]")
    console.print(len(memories))

    conn.close()


if __name__ == "__main__":
    main()
