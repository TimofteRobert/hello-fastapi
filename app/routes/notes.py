from fastapi import APIRouter, HTTPException
from app.database import get_connection
from app.models import Note, NoteCreate, NoteResponse
from app.services.notes_service import (
    get_notes,
    create_note,
    update_note,
    delete_note,
    get_note_by_id
    )

router = APIRouter()


@router.post("/notes", response_model=NoteResponse)
def create_note_route(note: NoteCreate):
    return create_note(note)


@router.get("/notes", response_model=list[NoteResponse])
def get_all_notes():
    return get_notes()


@router.get("/notes/{note_id}", response_model=NoteResponse)
def get_note_route(note_id: int):
    note = get_note_by_id(note_id)

    if note is Note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return note


@router.put("/notes/{note_id}", response_model=NoteResponse)
def update_note_route(note_id: int, note: NoteCreate):
    return update_note(note_id, note)


@router.delete("/notes/{note_id}")
def delete_note_route(note_id: int):
    result = delete_note(note_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return result
