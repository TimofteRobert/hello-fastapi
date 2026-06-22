// Stores the note currently being edited
let editingNoteId = null;

// UI helper functions
function setStatus(message) {
    document.getElementById("status").textContent = message;
}


function editNote(note) {
    document.getElementById("title").value = note.title;
    document.getElementById("content").value = note.content;
    editingNoteId = note.id;

    setStatus(`Editing note #${note.id}`);
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

    await createNoteApi(note);

    clearForm();
    loadNotes();

    setStatus("Creating new note");
    
}


function renderNotes(notes) {

    const container = document.getElementById("notes");

    container.innerHTML = "";

    notes.forEach(note => {
        container.appendChild(
            createNoteElement(note)
        );
    });
}

function createNoteElement(note) {

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

        return element;
}


// Load all notes from the backend API
async function loadNotes() {
    const notes = await getNotes();

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

    await deleteNoteApi(noteId);

    // Refresh UI after successful deletion
    loadNotes();
}


async function updateNote() {
    if (editingNoteId === null) {
        alert("Select a note first.");
        return;
    }

    const note = getFormData();

    await updateNoteApi(editingNoteId, note);

    editingNoteId = null;

    clearForm();
    loadNotes();

    setStatus("Creating new note");
}