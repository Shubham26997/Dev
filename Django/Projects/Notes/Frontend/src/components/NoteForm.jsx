import { useState } from "react";

export default function NoteForm({
    initialData = {},
    onSubmit,
    isEdit = false,
}) {
    const safeData = initialData || {};
    const [title, setTitle] = useState(safeData.title || "");
    const [content, setContent] = useState(safeData.content || "");
    const [completed, setCompleted] = useState(safeData.completed || false);

    return (
    <form
        className="space-y-4"
        onSubmit={(e) => {
        e.preventDefault();
        onSubmit({ title, content, completed });
        }}
    >
        <h2 className="text-xl font-semibold">
        {isEdit ? "Edit Note" : "Add Note"}
        </h2>

        <input
        className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500"
        placeholder="Title"
        value={title}
        required
        onChange={(e) => setTitle(e.target.value)}
        />

        <textarea
        className="w-full border rounded-lg px-3 py-2 h-28 focus:ring-2 focus:ring-indigo-500"
        placeholder="Content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        />

        {isEdit && (
        <label className="flex items-center gap-2 text-sm">
            <input
            type="checkbox"
            checked={completed}
            onChange={(e) => setCompleted(e.target.checked)}
            className="accent-indigo-600"
            />
            Mark as completed
        </label>
        )}

        <button
        type="submit"
        className="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition"
        >
        {isEdit ? "Update Note" : "Create Note"}
        </button>
    </form>
    );
}
