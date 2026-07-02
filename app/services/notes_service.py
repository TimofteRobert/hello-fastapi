from app.database import get_connection
from app.models import Note
from typing import Optional


# Create a new database connection and cursor
def get_cursor():
    conn = get_connection()
    cur = conn.cursor()

    return conn, cur


# Create a dictionary
def make_note(id, title, content):
    return {
        "id": id,
        "title": title,
        "content": content
    }


def get_notes(search: Optional[str] = None, sort: str = "id"):
    conn, cur = get_cursor()

    try:
        # Map allowed sort options to SQL
        sort_options = {
            "id": "id ASC",
            "id_desc": "id DESC",
            "title": "title ASC",
            "title_desc": "title DESC"
        }

        order_by = sort_options.get(sort, "id ASC")

        if search:
            cur.execute(
                f"""
                SELECT id, title, content
                FROM notes
                WHERE
                    title ILIKE %s
                    OR content ILIKE %s
                ORDER BY {order_by}
                """,
                (f"%{search}%", f"%{search}%")
            )
        else:
            cur.execute(
                f"""
                SELECT id, title, content
                FROM notes
                ORDER BY {order_by}
                """
                )

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
    conn, cur = get_cursor()

    try:
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
    conn, cur = get_cursor()

    try:
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
    conn, cur = get_cursor()

    try:
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
    conn, cur = get_cursor()

    try:
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
