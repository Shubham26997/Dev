import NotesPage from "./pages/NotesPage";

export default function App() {
    return (
        <div className="min-h-screen">
            <header className="bg-white shadow-md px-6 py-4">
        <h1 className="text-2xl font-bold text-indigo-600">
            Notes / Todos
        </h1>
        </header>

        <main className="max-w-4xl mx-auto px-4 py-6">
            <NotesPage />
        </main>
    </div>
    );
}
