from app.core.redis import redis_connection
from app.worker.document_worker import process_document
from rq import Queue,Retry


document_queue = Queue(
    "documents",
    connection=redis_connection,
)


def enqueue_document_processing(
    document_id: int,
):
    print("document ready for inequeue")
    job = document_queue.enqueue(
    process_document,
    document_id,
    retry=Retry(
        max=3,
        interval=[10, 30, 60],
    ),
)

    return job.id
