export default function SearchBar({ onSearch }) {
    return (
    <input
        type="text"
        placeholder="Search notes..."
        className="w-full sm:w-64 px-4 py-2 rounded-lg border focus:outline-none focus:ring-2 focus:ring-indigo-500"
        onChange={e => onSearch(e.target.value)}
    />
    );
}
