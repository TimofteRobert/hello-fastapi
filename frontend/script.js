// Stores the note currently being edited
let editingNoteId = null;

// UI helper functions
function setStatus(message) {
    document.getElementById("status").textContent = message;
}


// Error handling functions
function setError(message) {
    document.getElementById("status").textContent =
        `Error: ${message}`;
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

// Note operations
async function createNote() {
    try {
        setStatus("Creating note...");

        const note = getFormData();

        await createNoteApi(note);

        clearForm();
        loadNotes();

        setStatus("Creating new note");
    }
    catch (error) {
        console.error(error);
        setError("Could not create note");
    }
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

    try{
        setStatus("Loading notes...");

        const notes = await getNotes();
        renderNotes(notes);

        setStatus("Ready");
    }
    catch (error) {
        console.error(error);
        setError("Could not load notes from server");
    }
}

loadNotes();


async function deleteNote(noteId) {

    const confirmed = confirm(
        "Are you sure you want to delete this note?"
    );

    if (!confirmed) {
        return;
    }

    try {
        setStatus("Deleting note...");

        await deleteNoteApi(noteId);
    }
    catch (error) {
        setError("Could not delete note");
    }

    // Refresh UI after successful deletion
    loadNotes();
}


async function updateNote() {
    if (editingNoteId === null) {
        alert("Select a note first.");
        return;
    }

    try {
        setStatus("Updating note...");

        const note = getFormData();

        await updateNoteApi(editingNoteId, note);

        editingNoteId = null;

        clearForm();
        loadNotes();

        setStatus("Creating new note");
    }
    catch (error) {
        console.error(error);
        setError("Could not update note");
    }
}