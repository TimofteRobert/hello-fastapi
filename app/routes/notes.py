from fastapi import APIRouter
from app.database import get_connection
from app.models import Note
from app.services.notes_service import (
    get_notes,
    create_note,
    update_note,
    delete_note
    )

router = APIRouter()


@router.post("/notes")
def create_note_route(note: Note):
    return create_note(note)


@router.get("/notes")
def get_all_notes():
    return get_notes()


@router.put("/notes/{note_id}")
def update_note_route(note_id: int, note: Note):
    return update_note(note_id, note)


@router.delete("/notes/{note_id}")
def delete_note_route(note_id: int):
    return delete_note(note_id)
