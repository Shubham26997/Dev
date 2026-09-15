import api from "./client";

/* LIST NOTES */
export async function fetchNotes(params = {}) {
    const res = await api.get("/note/", { params });

    return {
        notes: normalizeList(res.data.data),
        message: res.data.message,
    };
}

/* CREATE NOTE */
export async function createNote(data) {
    const res = await api.post("/note/", {
        title: data.title,
        content: data.content,
    });

    return {
        note: normalizeNote(res.data.data),
        message: res.data.message,
    };
}

/* UPDATE NOTE */
export async function updateNote(id, data) {
    const res = await api.put(`/note/${id}/`, {
        title: data.title,
        content: data.content,
        is_completed: data.completed,
    });

    return {
        note: normalizeNote(res.data.data),
        message: res.data.message,
    };
}

/* DELETE NOTE */
export async function deleteNote(id) {
    const res = await api.delete(`/note/${id}/`);

    return {
        message: res.data.message,
    };
}

/* ---------------- HELPERS ---------------- */

function normalizeNote(note) {
    if (!note) return null;

    return {
        id: note.id,
        title: note.title,
        content: note.content,
        completed: note.is_completed,
        created_date: note.created_date,
        last_updated: note.last_updated || null,
    };
}

function normalizeList(list) {
    if (!Array.isArray(list)) return [];
    return list.map(normalizeNote);
}
