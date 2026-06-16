from app.database import get_connection
from app.models import Note

def get_notes():
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("SELECT id, title, content FROM notes")
        rows = cur.fetchall()

        return [
        {
            "id": r[0],
            "title": r[1],
            "content": r[2]
        }
        for r in rows
    ]

    finally:   
        cur.close() 
        conn.close()   


def get_note_by_id(note_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute(
            "SELECT id, title, content FROM notes WHERE id = %s",
            (note_id,)
        )

        row = cur.fetchone()

        if row is None:
            return None
    
        return {
            "id": row[0],
            "title": row[1],
            "content": row[2]
        }

    finally:
        cur.close()
        conn.close()

    
def create_note(note: Note):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO notes (title, content) VALUES (%s, %s) RETURNING id",
            (note.title, note.content)
        )

        note_id = cur.fetchone()[0]
        conn.commit()

        return {
            "id": note_id,
            "title": note.title,
            "content": note.content
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()    

def update_note(note_id: int, note: Note):
    conn = get_connection()

    try:
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

        if cur.rowcount == 0:
            return None

        conn.commit()

        return {
            "message": "Note updated",
            "id": note_id,
            "title": note.title,
            "content": note.content
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()


def delete_note(note_id: int):
    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM notes WHERE id = %s",
            (note_id,)
        )

        if cur.rowcount == 0:
            return None

        conn.commit()

        return {
            "message": "Note deleted",
            "id": note_id
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()
