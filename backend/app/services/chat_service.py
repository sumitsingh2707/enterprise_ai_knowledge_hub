def ask_question(
    question: str,
    history=None,
    thread_id: str | None = None,
    rag_graph=None,
):
    """
    Execute the LangGraph RAG workflow
    using PostgreSQL checkpointing.
    """

    if rag_graph is None:
        raise ValueError(
            "RAG graph has not been initialized."
        )

    if not thread_id:
        raise ValueError(
            "thread_id is required."
        )

    initial_state = {
        "question": question,
        "history": history or [],
        "retrieval_attempts": 0,
    }

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    result = rag_graph.invoke(
        initial_state,
        config=config,
    )

    return {
        "answer": result.get(
            "answer",
            "I could not generate an answer.",
        ),
        "sources": result.get(
            "sources",
            [],
        ),
    }