from fastapi import APIRouter

router = APIRouter()

@router.get("/projects")
def projects():

    return [
        {
            "name": "Vasuki Core",
            "description": "Personal Intelligence System",
            "evidence": "41802 files indexed"
        },
        {
            "name": "Janani",
            "description": "Founder Discipline Engine",
            "evidence": "21422 memories"
        }
    ]
