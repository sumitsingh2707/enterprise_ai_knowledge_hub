from langgraph.graph import (
    StateGraph,
    END,
)

from app.graph.state import GraphState
from app.graph.nodes import (
    rewrite_question,
    retrieve_documents,
    evaluate_retrieval,
    build_context_node,
    generate_answer,
    fallback_answer,
)



def should_generate_answer(
    state: GraphState,
) -> str:

    if state.get("relevant", False):
        return "build_context"

    attempts = state.get(
        "retrieval_attempts",
        0,
    )

    if attempts < 2:
        return "rewrite_question"

    return "fallback"


def create_workflow(checkpointer):

    graph = StateGraph(GraphState)

    # ---------------------------------------------
    # Nodes
    # ---------------------------------------------

    graph.add_node(
        "rewrite_question",
        rewrite_question,
    )

    graph.add_node(
        "retrieve_documents",
        retrieve_documents,
    )

    graph.add_node(
        "evaluate_retrieval",
        evaluate_retrieval,
    )

    graph.add_node(
        "build_context",
        build_context_node,
    )

    graph.add_node(
        "generate_answer",
        generate_answer,
    )

    graph.add_node(
        "fallback",
        fallback_answer,
    )

    # ---------------------------------------------
    # Entry point
    # ---------------------------------------------

    graph.set_entry_point(
        "rewrite_question"
    )

    # ---------------------------------------------
    # Main flow
    # ---------------------------------------------

    graph.add_edge(
        "rewrite_question",
        "retrieve_documents",
    )

    graph.add_edge(
        "retrieve_documents",
        "evaluate_retrieval",
    )

    # ---------------------------------------------
    # Conditional routing
    # ---------------------------------------------

    graph.add_conditional_edges(
        "evaluate_retrieval",
        should_generate_answer,
        {
            "build_context": "build_context",
            "rewrite_question": "rewrite_question",
            "fallback": "fallback",
        },
    )

    # ---------------------------------------------
    # Generate answer
    # ---------------------------------------------

    graph.add_edge(
        "build_context",
        "generate_answer",
    )

    graph.add_edge(
        "generate_answer",
        END,
    )

    graph.add_edge(
        "fallback",
        END,
    )

    return graph.compile(checkpointer=checkpointer)


