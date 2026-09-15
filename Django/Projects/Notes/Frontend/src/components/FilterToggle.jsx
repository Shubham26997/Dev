export default function FilterToggle({ onToggle }) {
    return (
    <label className="flex items-center gap-2 text-sm">
        <input
        type="checkbox"
        className="accent-indigo-600"
        onChange={e => onToggle(e.target.checked)}
    />
    Show completed only
    </label>
    );
}
