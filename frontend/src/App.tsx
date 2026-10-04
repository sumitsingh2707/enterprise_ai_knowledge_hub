import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
import Documents from "./pages/document";
import Chat from "./pages/chat"

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Dashboard</Link>{" "}
        <Link to="/documents">Documents</Link>
        <Link to="/chat">AI Copilot</Link>
      </nav>

      <Routes>
        <Route
          path="/"
          element={
            <div>
              <h1>Enterprise AI Copilot</h1>
            </div>
          }
        />

        <Route
          path="/documents"
          element={<Documents />}
        />
        <Route
          path="/chat"
          element={<Chat />}
        />
      </Routes>

    </BrowserRouter>
  );
}

export default App;