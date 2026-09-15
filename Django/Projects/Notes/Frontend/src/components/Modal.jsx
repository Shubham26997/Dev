export default function Modal({ children, onClose }) {
    return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl shadow-lg w-full max-w-md p-6 relative">
        <button
            className="absolute top-3 right-3 text-gray-400 hover:text-gray-600"
            onClick={onClose}
        >
        ✕
        </button>
        {children}
        </div>
    </div>
    );
}
