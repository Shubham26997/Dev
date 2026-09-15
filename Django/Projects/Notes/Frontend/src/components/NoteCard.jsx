export default function NoteCard({ note, onEdit, onDelete }) {
    return (
    <div className="bg-white rounded-xl shadow-sm p-4 flex justify-between">
        <div>
            <h3 className="font-semibold text-lg">{note.title}</h3>
            <p className="text-sm text-gray-600 mt-1">
            {note.content || "No content"}
        </p>

        <span
            className={`inline-block mt-2 px-3 py-1 text-sm rounded-full ${
            note.completed
                ? "bg-green-100 text-green-700"
                : "bg-yellow-100 text-yellow-700"
            }`}
        >
            {note.completed ? "Completed" : "Pending"}
        </span>
        </div>

        <div className="flex flex-col gap-2">
        <button
            onClick={onEdit}
            className="px-3 py-1 text-sm rounded-lg bg-gray-100 hover:bg-gray-200"
        >
            Edit
        </button>

        <button
            onClick={onDelete}
            className="px-3 py-1 text-sm rounded-lg bg-red-100 text-red-600 hover:bg-red-200"
        >
            Delete
        </button>
        </div>
    </div>
    );
}
