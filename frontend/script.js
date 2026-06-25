// Stores the note currently being edited
let editingNoteId = null;

// UI helper functions
function setStatus(message) {
    document.getElementById("status").textContent = message;
}


// Validate note form data
function validateNote(note) {
    if (note.title.trim() === "") {
        setError("Title cannot be empty");
        return false;
    }

    if (note.content.trim() === "") {
        setError("Content cannot be empty");
        return false;
    }

    if (note.title.trim().length < 3) {
        setError("Title must be at least 3 characters")
        return false;
    }

    if (note.content.trim().length < 5) {
        setError("Content must be at least 5 characters")
        return false;
    }

    return true;
}


// Enable or disable action buttons
function setButtonsDisabled(disabled) {
    const buttons = document.querySelectorAll("button");

    buttons.forEach(button => {
        button.disabled = disabled;
    });
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
    setButtonsDisabled(true);

    try {
        const note = getFormData();

        if (!validateNote(note)) {
            return;
        }

        await createNoteApi(note);   

        clearForm();
        loadNotes();

        setStatus("Note created successfully");
    }
    catch (error) {
        console.error(error);
        setError("Could not create note");
    }
    finally {
        setButtonsDisabled(false);
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

    setButtonsDisabled(true);

    try {
        await deleteNoteApi(noteId);

        setStatus("Note deleted successfully");
    }
    catch (error) {
        setError("Could not delete note");
    }
    finally {
        setButtonsDisabled(false);
    }

    // Refresh UI after successful deletion
    loadNotes();
}


async function updateNote() {
    if (editingNoteId === null) {
        alert("Select a note first.");
        return;
    }

    setButtonsDisabled(true);

    try {
        const note = getFormData();

        if (!validateNote(note)) {
            return;
        }

        await updateNoteApi(editingNoteId, note);

        editingNoteId = null;

        clearForm();
        loadNotes();

        setStatus("Note updated successfully");
    }
    catch (error) {
        console.error(error);
        setError("Could not update note");
    }
    finally {
        setButtonsDisabled(false);
    }
}