from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    conversation_id: int | None = None


class ChatSource(BaseModel):
    document_id: int
    file_name: str
    page: int
    chunk_index: int
    score: float


class ChatResponse(BaseModel):
    conversation_id: int
    answer: str
    sources: list[ChatSource]