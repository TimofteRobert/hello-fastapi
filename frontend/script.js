let editingNoteId = null;


function editNote(note) {
    document.getElementById("title").value = note.title;
    document.getElementById("content").value = note.content;
    editingNoteId = note.id;
}


async function createNote() {
    const title = document.getElementById("title").value;
    const content = document.getElementById("content").value;

    await fetch(
        "http://127.0.0.1:8000/notes",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: title,
                content: content
            })
        }
    );

    document.getElementById("title").value = "";
    document.getElementById("content").value = "";

    loadNotes();
}


function renderNotes(notes) {

    const container = document.getElementById("notes");
    container.innerHTML = "";
    notes.forEach(note => {
        const element = document.createElement("p");
        element.innerHTML =
        `
        ${note.id}: ${note.title} - ${note.content}

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


async function loadNotes() {
    const response = await fetch(
        "http://127.0.0.1:8000/notes"
    );

    const notes = await response.json();

    renderNotes(notes);
}

loadNotes();


async function deleteNote(noteId) {
    await fetch(
        `http://127.0.0.1:8000/notes/${noteId}`,
        {
            method: "DELETE"
        }
    );

    loadNotes();
}


async function updateNote() {
    if (editingNoteId === null) {
        alert("Select a note first.");
        return;
    }

    const title = document.getElementById("title").value;
    const content = document.getElementById("content").value;

    await fetch(
        `http://127.0.0.1:8000/notes/${editingNoteId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: title,
                content: content
            })
        }
    );

    editingNoteId = null;

    document.getElementById("title").value = "";
    document.getElementById("content").value = "";

    loadNotes();
}