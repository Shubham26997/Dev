import { useEffect } from "react";

export default function Toast({ message, onClose }) {
    useEffect(() => {
    const t = setTimeout(onClose, 3000);
    return () => clearTimeout(t);
    }, []);

    return (
    <div className="fixed top-6 right-6 bg-indigo-600 text-white px-4 py-2 rounded-lg shadow-lg animate-fade-in">
        {message}
    </div>
    );
}
