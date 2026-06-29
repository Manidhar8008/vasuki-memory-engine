from memory import save_memory
from memory import recent
from brain import think


def handle(command):

    text = command.strip()

    if text.startswith("remember"):

        content = text.replace("remember","",1).strip()

        save_memory(content)

        return "✓ Memory stored."

    if text == "recent":

        rows = recent()

        if not rows:
            return "No memories."

        return "\n".join(
            f"- {x['content']}"
            for x in rows
        )

    if text.startswith("ask"):

        q = text.replace("ask","",1).strip()

        return think(q)

    if text == "status":

        return """
VASUKI STATUS

Kernel  ✅

Memory  ✅

Brain   ✅

Ready.
"""

    if text == "help":

        return """
remember <text>

recent

ask <question>

status

exit
"""

    return "Unknown command."
