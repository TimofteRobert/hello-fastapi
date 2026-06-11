from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}

@app.get("/about")
def about():
    return {
        "name": "Robert",
        "learning": "FastAPI"
    }

class Note(BaseModel):
    title: str
    content: str

@app.post("/notes")
def create_note(note: Note):
    return {
        "message": "Note created",
        "note": note
    }

@app.get("/notes")
def notes():
    return [
        {"id": 1, "title": "Learn Git"},
        {"id": 2, "title": "Learn FastAPI"}
    ]