from fastapi import FastAPI

from routes.stats import router as stats_router
from routes.projects import router as projects_router
from routes.skills import router as skills_router
from routes.ask import router as ask_router

app = FastAPI(title="Vasuki Portfolio API")

app.include_router(stats_router,prefix="/api")
app.include_router(projects_router,prefix="/api")
app.include_router(skills_router,prefix="/api")
app.include_router(ask_router,prefix="/api")

@app.get("/")
def root():
    return {
        "status":"online",
        "name":"Vasuki Portfolio API"
    }
