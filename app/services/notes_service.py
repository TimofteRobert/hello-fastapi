from app.database import get_connection
from app.models import Note
from typing import Optional


# Create a new database connection and cursor
def get_cursor():
    conn = get_connection()
    cur = conn.cursor()

    return conn, cur


# Close database resources
def close_cursor(conn, cur):
    cur.close()
    conn.close()


# Create a dictionary
def make_note(note_id, title, content):
    return {
        "id": note_id,
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
            make_note(
                r[0],
                r[1],
                r[2]
            )
            for r in rows
        ]

    finally:   
        close_cursor(conn, cur)  


def get_note_stats(search: Optional[str] = None):
    conn, cur = get_cursor()

    try:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM notes
            """
        )
        total_notes = cur.fetchone()[0]

        if search:
            cur.execute(
                """
                SELECT COUNT(*)
                FROM notes
                WHERE 
                    title ILIKE %s
                    OR content ILIKE %s
                """,
                (f"%{search}%", f"%{search}%")
            )
            matching_notes = cur.fetchone()[0] 
        else:
            matching_notes = total_notes

               

        return {
            "total_notes": total_notes,
            "matching_notes": matching_notes
        }
    
    finally:
        close_cursor(conn, cur)  


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
    
        return make_note(
            row[0],
            row[1],
            row[2]
        )

    finally:
        close_cursor(conn, cur)  

    
def create_note(note: Note):
    conn, cur = get_cursor()

    try:
        cur.execute(
            "INSERT INTO notes (title, content) VALUES (%s, %s) RETURNING id",
            (note.title, note.content)
        )

        note_id = cur.fetchone()[0]
        conn.commit()

        return make_note(
            note_id,
            note.title,
            note.content
        )

    except Exception:
        conn.rollback()
        raise

    finally:
        close_cursor(conn, cur)     

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

        updated_note = make_note(
            note_id,
            note.title,
            note.content
        )
        updated_note["message"] = "Note updated"

        return updated_note

    except Exception:
        conn.rollback()
        raise

    finally:
        close_cursor(conn, cur)  


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
        close_cursor(conn, cur)  
