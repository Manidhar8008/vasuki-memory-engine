from fastapi import APIRouter

router = APIRouter()

@router.get("/ask")
def ask(q:str):

    q=q.lower()

    if "vasuki" in q:
        return {
            "answer":"Vasuki indexed 41802 files and extracted 42648 entities."
        }

    if "janani" in q:
        return {
            "answer":"Janani is the founder discipline and reflection system."
        }

    return {
        "answer":"No answer available."
    }
