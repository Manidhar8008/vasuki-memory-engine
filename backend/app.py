from fastapi import FastAPI

app = FastAPI(title="Vasuki Explorer")


@app.get("/")
def root():
    return {
        "status": "online"
    }


@app.get("/stats")
def stats():
    return {
        "documents": 595,
        "entities": 42648,
        "evidence": 1239,
        "timeline": 165
    }


@app.get("/whoami")
def whoami():
    return {
        "title": "AI Systems Builder",
        "focus": "Personal Intelligence Infrastructure",
        "mission": "Building systems that transform information into understanding"
    }


@app.get("/projects")
def projects():
    return [
        {
            "name": "Vasuki",
            "description": "Personal Intelligence OS"
        },
        {
            "name": "Janani",
            "description": "Discipline Engine"
        },
        {
            "name": "MW.AI",
            "description": "AI Systems for Businesses"
        }
    ]


@app.get("/knowledge")
def knowledge():
    return [
        "AI",
        "Data Engineering",
        "Systems Design",
        "Knowledge Graphs",
        "Automation",
        "Python",
        "FastAPI"
    ]
