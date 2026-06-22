import os
import re

CORE = "./founder_core"

themes = {
    "memory": 0,
    "agent": 0,
    "timeline": 0,
    "graph": 0,
    "search": 0,
    "rag": 0,
    "project": 0,
    "cognitive": 0,
    "sqlite": 0,
    "knowledge": 0,
}

for file in os.listdir(CORE):

    path = os.path.join(CORE, file)

    try:

        with open(path, "r", encoding="utf-8", errors="ignore") as f:

            text = f.read().lower()

            for theme in themes:

                themes[theme] += text.count(theme)

    except:
        pass

print("\nFOUNDER PSYCHOLOGIST\n")

for k, v in sorted(
    themes.items(),
    key=lambda x: x[1],
    reverse=True
):

    print(f"{k:15} {v}")

