from providers.nvidia import ask_nvidia
from memory import search


def think(question):

    memories = search(question)

    if memories:

        context = "\n".join(
            x["content"]
            for x in memories
        )

        return f"Memory:\n\n{context}"

    return ask_nvidia(question)
