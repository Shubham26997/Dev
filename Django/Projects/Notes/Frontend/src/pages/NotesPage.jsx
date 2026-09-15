import { useEffect, useState } from "react";
import { fetchNotes, createNote, deleteNote, updateNote} from "../api/notes";
import NoteCard from "../components/NoteCard";
import SearchBar from "../components/SearchBar";
import FilterToggle from "../components/FilterToggle";
import Toast from "../components/Toast";
import Modal from "../components/Modal";
import NoteForm from "../components/NoteForm";


export default function NotesPage() {
    const [editingNote, setEditingNote] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const [notes, setNotes] = useState([]);
    const [search, setSearch] = useState("");
    const [showCompleted, setShowCompleted] = useState(false);
    const [toast, setToast] = useState(null);

    useEffect(() => {
    fetchNotes()
    .then(({ notes, message }) => {
        setNotes(notes);
        setToast(message);
    })
    .catch(() => {
        setToast("Failed to load notes");
    });
    }, []);


    const filtered = notes.filter(n =>
    n.title.toLowerCase().includes(search.toLowerCase()) &&
    (showCompleted ? n.completed : true)
    );

    return (
    <div className="space-y-6">
    {/* Controls */}
    <div className="flex flex-col sm:flex-row gap-4 sm:items-center sm:justify-between">
        <SearchBar onSearch={setSearch} />
        <FilterToggle onToggle={setShowCompleted} />
    </div>

    {/* Add button */}
    <button
    className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
    onClick={() => {
        setEditingNote(null);
        setShowModal(true);
    }}
    >
    + Add Note
    </button>

    {/* Notes */}
    <div className="grid gap-4">
        {filtered.map(note => (
        <NoteCard
            key={note.id}
            note={note}
            onEdit={() => {
            setEditingNote(note);
            setShowModal(true);
            }}
            onDelete={() => {
                deleteNote(note.id)
                .then(({ message }) => {
                setNotes(notes.filter(n => n.id !== note.id));
                setToast(message);
                })
            .catch(() => setToast("Delete failed"));
            }}

        />
        ))}
    </div>
        {showModal && (
    <Modal onClose={() => setShowModal(false)}>
    <NoteForm
        initialData={editingNote}
        isEdit={!!editingNote}
        onSubmit={(data) => {
            if (editingNote) {
                updateNote(editingNote.id, data)
                    .then(({ note, message }) => {
                    setNotes(notes.map(n =>
                    n.id === note.id ? note : n
                ));
                setToast(message);
                })
                .catch(() => setToast("Update failed"));
            } else {
                createNote(data)
                .then(({ note, message }) => {
                setNotes([note, ...notes]);
                setToast(message);
                })
            .catch(() => setToast("Create failed"));
            }

            setShowModal(false);
            }}

        />
    </Modal>
    )}
    {toast && <Toast message={toast} onClose={() => setToast(null)} />}
    </div>
    );

}
