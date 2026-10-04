import { useEffect, useState } from "react";

interface Document {
    id: number;
    file_name: string;
    file_type: string;
    file_size: number;
    status: string;
    created_at: string;
}

function Documents() {
    const [documents, setDocuments] = useState<Document[]>([]);
    const [loading, setLoading] = useState(true);

    const loadDocuments = async () => {
        try {
            const response = await fetch("http://localhost:8000/api/documents");
            const data = await response.json();
            setDocuments(data)
        } catch (error) {
            console.error("failed to load documents", error)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        loadDocuments()
    }, [])

    const uploadDocument = async (
        event: React.ChangeEvent<HTMLInputElement>
    ) => {
        const file = event.target.files?.[0];

        if (!file) {
            return;
        }

        const formData = new FormData();

        formData.append("file", file);

        try {
            const response = await fetch(
                "http://localhost:8000/api/documents",
                {
                    method: "POST",
                    body: formData,
                }
            );

            if (!response.ok) {
                throw new Error("Upload failed");
            }

            await loadDocuments();
        } catch (error) {
            console.error("Failed to upload document", error);
        }
    };

    if (loading) {
        return <p>Loading documents...</p>;
    }

    return (
        <div>
            <h1>Knowledge Base</h1>

            <label>
                Upload Document

                <input
                    type="file"
                    accept=".pdf,.docx,.txt"
                    onChange={uploadDocument}
                    hidden
                />
            </label>

            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Type</th>
                        <th>Size</th>
                        <th>Status</th>
                    </tr>
                </thead>

                <tbody>
                    {documents.map((document) => (
                        <tr key={document.id}>
                            <td>{document.file_name}</td>
                            <td>{document.file_type}</td>
                            <td>{document.file_size} bytes</td>
                            <td>{document.status}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );

}

export default Documents;