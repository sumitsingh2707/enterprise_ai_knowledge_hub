from fastapi import (
    APIRouter,
    Depends,
    Request,
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.conversation import (
    Conversation,
)

from app.models.message import (
    Message,
)

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)

from app.services.chat_service import (
    ask_question,
)

from app.services.conversation_service import (
    get_conversation_history,
)


router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: Request,
    chat_request: ChatRequest,
    db: Session = Depends(get_db),
):

    conversation = None

    # -----------------------------------------
    # Find existing conversation
    # -----------------------------------------

    if chat_request.conversation_id:

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id
                == chat_request.conversation_id
            )
            .first()
        )

    # -----------------------------------------
    # Create conversation
    # -----------------------------------------

    if not conversation:

        conversation = Conversation(
            title=chat_request.question[:100],
            user_id=1,
        )

        db.add(conversation)

        db.commit()

        db.refresh(conversation)

    # -----------------------------------------
    # Existing application history
    # -----------------------------------------

    history = get_conversation_history(
        db=db,
        conversation_id=conversation.id,
    )

    # -----------------------------------------
    # Save user message
    # -----------------------------------------

    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=chat_request.question,
    )

    db.add(user_message)

    db.commit()

    # -----------------------------------------
    # LangGraph thread
    # -----------------------------------------

    thread_id = str(
        conversation.id
    )

    # -----------------------------------------
    # Execute LangGraph
    # -----------------------------------------

    result = ask_question(
        question=chat_request.question,
        history=history,
        thread_id=thread_id,
        rag_graph=request.app.state.rag_graph,
    )

    # -----------------------------------------
    # Save assistant message
    # -----------------------------------------

    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=result["answer"],
    )

    db.add(assistant_message)

    db.commit()

    # -----------------------------------------
    # Response
    # -----------------------------------------

    return {
        "conversation_id": conversation.id,
        "answer": result["answer"],
        "sources": result["sources"],
    }