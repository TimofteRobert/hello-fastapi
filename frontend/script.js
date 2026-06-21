const API_URL = "http://127.0.0.1:8000";

// Stores the note currently being edited
let editingNoteId = null;


function editNote(note) {
    document.getElementById("title").value = note.title;
    document.getElementById("content").value = note.content;
    editingNoteId = note.id;

    document.getElementById("status").textContent =
        `Editing note #${note.id}`;
}


// Read values from the note form
function getFormData() {
    return {
        title: document.getElementById("title").value,
        content: document.getElementById("content").value
    };
}


// Reset the form after create/update
function clearForm() {
    document.getElementById("title").value = "";
    document.getElementById("content").value = "";
}


async function createNote() {
    const note = getFormData();

    await fetch(
        `${API_URL}/notes`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(note)
        }
    );

    clearForm();
    loadNotes();

    document.getElementById("status").textContent =
        "Creating new note";
    
}


function renderNotes(notes) {

    const container = document.getElementById("notes");
    container.innerHTML = "";
    notes.forEach(note => {
        const element = document.createElement("div");
        element.className = "note";
        element.innerHTML =
        `
        <h3>${note.title}</h3>
        <p>${note.content}</p>
        <small>ID: ${note.id}</small>
        <br /><br />

        <button onclick='editNote(${JSON.stringify(note)})'>
            Edit
        </button>

        <button onclick="deleteNote(${note.id})">
            Delete
        </button>
        `;

        container.appendChild(element);

    });
}


// Load all notes from the backend API
async function loadNotes() {
    const response = await fetch(
        `${API_URL}/notes/`
    );

    const notes = await response.json();

    renderNotes(notes);
}

loadNotes();


async function deleteNote(noteId) {

    const confirmed = confirm(
        "Are you sure you want to delete this note?"
    );

    if (!confirmed) {
        return;
    }

    await fetch(
        `${API_URL}/notes/${noteId}`,
        {
            method: "DELETE"
        }
    );

    // Refresh UI after successful deletion
    loadNotes();
}


async function updateNote() {
    if (editingNoteId === null) {
        alert("Select a note first.");
        return;
    }

    const note = getFormData();

    await fetch(
        `${API_URL}/notes/${editingNoteId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(note)
        }
    );

    editingNoteId = null;

    clearForm();
    loadNotes();

    document.getElementById("status").textContent =
        "Creating new note";
}