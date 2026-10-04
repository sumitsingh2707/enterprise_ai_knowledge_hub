from typing import TypedDict, Any


class GraphState(TypedDict, total=False):
    question: str
    rewritten_question: str

    history: list[Any]

    retrieved_documents: list[Any]

    context: str

    answer: str

    sources: list[dict]

    retrieval_attempts: int

    relevant: bool
