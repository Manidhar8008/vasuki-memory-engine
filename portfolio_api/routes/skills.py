from fastapi import APIRouter

router = APIRouter()

@router.get("/skills")
def skills():
    return [
        "Python",
        "FastAPI",
        "SQLite",
        "Knowledge Graphs",
        "NLP",
        "Systems Design"
    ]
