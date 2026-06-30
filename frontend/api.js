const API_URL = "http://127.0.0.1:8000";


// Get all notes
async function getNotes(search = "") {
    const response = await fetch(
        `${API_URL}/notes?search=${encodeURIComponent(search)}`
    );

    if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
    }

    return await response.json();
}


// Create note
async function createNoteApi(note) {
    const response = await fetch(
        `${API_URL}/notes`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(note)
        }
    );

    
    if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
    }

    return await response.json();
}


// Update note
async function updateNoteApi(noteId, note) {
    const response = await fetch(
        `${API_URL}/notes/${noteId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(note)
        }
    );

    
    if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
    }

    return await response.json();
}


// Delete note
async function deleteNoteApi(noteId) {
    const response = await fetch(
        `${API_URL}/notes/${noteId}`,
        {
            method: "DELETE"
        }
    );

    
    if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
    }
}
