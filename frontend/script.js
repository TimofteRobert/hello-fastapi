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

    loadNotes();
}

async function loadNotes() {
    const response = await fetch(
        "http://127.0.0.1:8000/notes"
    );

    const notes = await response.json();

    const container = document.getElementById("notes");

    container.innerHTML = "";

    notes.forEach(note => {
        const element = document.createElement("p");

        element.innerHTML =
        `${note.id}: ${note.title} - ${note.content}`;

        container.appendChild(element);
    });
}

loadNotes();