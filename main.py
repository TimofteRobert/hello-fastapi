from fastapi import FastAPI
from pydantic import BaseModel
from database import get_connection

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
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO notes (title, content) VALUES (%s, %s) RETURNING id",
        (note.title, note.content)
    )

    note_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return {
        "id": note_id,
        "title": note.title,
        "content": note.content
    }

@app.get("/notes")
def get_notes():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, title, content FROM notes")
    rows = cur.fetchall()

    conn.close()

    return [
        {"id": r[0], "title": r[1], "content": r[2]}
        for r in rows
    ]

@app.put("/notes/{note_id}")
def update_note(note_id: int, note: Note):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE notes
        SET title = %s,
            content = %s
        WHERE id = %s
        """,
        (note.title, note.content, note_id)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Note updated",
        "id": note_id,
        "title": note.title,
        "content": note.content
    }

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM notes WHERE id = %s",
        (note_id,)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Note deleted",
        "id": note_id
    }