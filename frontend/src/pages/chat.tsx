import { useState } from "react";
import { API_URL } from "../config/api";

interface Source {
  document_id: number;
  file_name: string;
  page: number;
  chunk_index: number;
  score: number;
}

interface ChatResponse {
  conversation_id: number;
  answer: string;
  sources: Source[];
}

function Chat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<Source[]>([]);
  const [conversationId, setConversationId] =
    useState<number | null>(null);

  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!question.trim()) {
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/api/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question,
            conversation_id: conversationId,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Chat request failed");
      }

      const data: ChatResponse =
        await response.json();

      setConversationId(
        data.conversation_id
      );

      setAnswer(data.answer);
      setSources(data.sources);
      setQuestion("");
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Enterprise AI Copilot</h1>

      <div>
        <h2>You</h2>

        <textarea
          value={question}
          onChange={(event) =>
            setQuestion(event.target.value)
          }
          placeholder="Ask your knowledge base..."
          rows={4}
        />

        <button
          onClick={sendMessage}
          disabled={loading}
        >
          {loading ? "Thinking..." : "Send"}
        </button>
      </div>

      {answer && (
        <div>
          <h2>Copilot</h2>

          <p>{answer}</p>

          <h3>Sources</h3>

          {sources.map((source) => (
            <div key={source.chunk_index}>
              📄 {source.file_name} —
              Page {source.page}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Chat;