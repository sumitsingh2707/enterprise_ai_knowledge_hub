from langchain_qdrant import QdrantVectorStore

from app.core.config import settings
from app.services.chunking import split_documents
from app.services.documents_loader_rag import load_document
from app.services.embeddings import embeddings


COLLECTION_NAME = "enterprise_ai_documents"


def ingest_document(
    file_path: str,
    file_type: str,
    document_id: int,
    file_name: str,
):
    documents = load_document(
        file_path,
        file_type,
    )

    if not documents:
        raise ValueError(
            "No text could be extracted from document"
        )

    chunks = split_documents(documents)

    for index, chunk in enumerate(chunks):
        chunk.metadata.update(
            {
                "document_id": document_id,
                "file_name": file_name,
                "chunk_index": index,
            }
        )

    vector_store = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        url=settings.qdrant_url,
    )

    return {
        "document_id": document_id,
        "chunks": len(chunks),
    }