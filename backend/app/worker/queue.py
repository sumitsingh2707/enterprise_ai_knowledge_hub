from rq import Queue

from app.core.redis import redis_connection


document_queue = Queue(
    "documents",
    connection=redis_connection,
)
