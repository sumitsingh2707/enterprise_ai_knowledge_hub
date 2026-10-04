from langchain_qdrant import QdrantVectorStore

from app.core.config import settings
from app.services.embeddings import embeddings


COLLECTION_NAME = "enterprise_ai_documents"


def get_vector_store() -> QdrantVectorStore:

    return QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        url=settings.qdrant_url,
    )