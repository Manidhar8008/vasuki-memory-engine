from fastapi import APIRouter

router = APIRouter()

@router.get("/projects")
def projects():
    return [
        {
            "name":"Vasuki Core",
            "description":"Personal Intelligence System"
        },
        {
            "name":"Janani",
            "description":"Founder Discipline Engine"
        }
    ]
