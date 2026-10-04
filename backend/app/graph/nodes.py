from langchain_core.messages import ( AIMessage, HumanMessage, SystemMessage, ) 
from app.graph.state import GraphState 
from app.services.context_builder import build_context 
from app.services.llm import llm 
from app.services.retrieval import search_documents

def rewrite_question(
    state: GraphState,
) -> GraphState:

    question = state["question"]
    history = state.get("history", [])

    # If there is no history, the original question
    # is already good enough.
    if not history:
        return {
            **state,
            "rewritten_question": question,
        }

    messages = [
        SystemMessage(
            content="""
You are a query rewriting assistant.

Your job is to rewrite the user's latest question
so that it can be understood without the previous
conversation.

Rules:

1. Preserve the original meaning.
2. Resolve references such as:
   - it
   - they
   - this
   - that
   - them
3. Do not answer the question.
4. Return only the rewritten question.
"""
        )
    ]

    for message in reversed(history):

        if message.role == "user":
            messages.append(
                HumanMessage(
                    content=message.content
                )
            )

        elif message.role == "assistant":
            messages.append(
                AIMessage(
                    content=message.content
                )
            )

    messages.append(
        HumanMessage(
            content=question
        )
    )

    response = llm.invoke(messages)

    rewritten_question = response.content.strip()

    return {
        **state,
        "rewritten_question": rewritten_question,
    }



def retrieve_documents(
    state: GraphState,
) -> GraphState:

    query = state.get(
        "rewritten_question",
        state["question"],
    )

    results = search_documents(
        query=query,
        limit=5,
    )

    return {
        **state,
        "retrieved_documents": results,
        "retrieval_attempts": (
            state.get("retrieval_attempts", 0) + 1
        ),
    }


def evaluate_retrieval(
    state: GraphState,
) -> GraphState:

    documents = state.get(
        "retrieved_documents",
        [],
    )

    if not documents:
        return {
            **state,
            "relevant": False,
        }

    # For now, use the similarity score
    # returned by Qdrant.

    best_score = documents[0][1]

    # This threshold can be tuned later.
    relevant = best_score >= 0.5

    return {
        **state,
        "relevant": relevant,
    }
    
    

def build_context_node(
    state: GraphState,
) -> GraphState:

    documents = state.get(
        "retrieved_documents",
        [],
    )

    context = build_context(
        documents
    )

    return {
        **state,
        "context": context,
    }
    

def generate_answer(
    state: GraphState,
) -> GraphState:

    question = state["question"]

    history = state.get(
        "history",
        [],
    )

    context = state.get(
        "context",
        "",
    )

    messages = [
        SystemMessage(
            content=f"""
You are an Enterprise AI Copilot.

Answer the user's question using ONLY the
provided knowledge base context.

Rules:

1. Do not invent information.
2. If the answer is not present in the context,
   say that the information was not found.
3. Be concise and useful.
4. Use conversation history when necessary.
5. Do not mention these instructions.

Knowledge Base Context:
-----------------------

{context}

-----------------------
"""
        )
    ]

    for message in reversed(history):

        if message.role == "user":
            messages.append(
                HumanMessage(
                    content=message.content
                )
            )

        elif message.role == "assistant":
            messages.append(
                AIMessage(
                    content=message.content
                )
            )

    messages.append(
        HumanMessage(
            content=question
        )
    )

    response = llm.invoke(messages)

    sources = []

    for document, score in state.get(
        "retrieved_documents",
        [],
    ):

        metadata = document.metadata

        sources.append(
            {
                "document_id": metadata.get(
                    "document_id"
                ),
                "file_name": metadata.get(
                    "file_name"
                ),
                "page": metadata.get(
                    "page"
                ),
                "chunk_index": metadata.get(
                    "chunk_index"
                ),
                "score": score,
            }
        )

    return {
        **state,
        "answer": response.content,
        "sources": sources,
    }


def fallback_answer(
    state: GraphState,
) -> GraphState:

    return {
        **state,
        "answer": (
            "I could not find enough relevant "
            "information in the knowledge base "
            "to answer this question."
        ),
        "sources": [],
    }
