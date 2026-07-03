from fastapi import APIRouter
from db import get_db

router = APIRouter()

@router.get("/stats")
def stats():

    conn = get_db()

    rows = conn.execute(
        "SELECT metric,value FROM stats"
    ).fetchall()

    conn.close()

    return {
        metric: value
        for metric, value in rows
    }

