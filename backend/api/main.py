from fastapi import FastAPI

from agents.archaeologist import search
from agents.relationship_mapper import get_relationships
from agents.identity_reconstructor import profile

app = FastAPI()

@app.get("/")
def root():

    return {
        "system":"VASUKI"
    }

@app.get("/search")
def query(q:str):

    return {
        "results":search(q)
    }

@app.get("/relationships")
def relationships():

    return {
        "data":get_relationships()
    }

@app.get("/identity")
def identity():

    return {
        "data":profile()
    }
