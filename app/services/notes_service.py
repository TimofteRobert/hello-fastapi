from app.database import get_connection
from app.models import Note

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