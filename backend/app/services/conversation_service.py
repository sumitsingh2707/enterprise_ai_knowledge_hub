from sqlalchemy.orm import Session

from app.models.message import Message


def get_conversation_history(
    db: Session,
    conversation_id: int,
    limit: int = 10,
):
    return (
        db.query(Message)
        .filter(
            Message.conversation_id
            == conversation_id
        )
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )