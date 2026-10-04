from fastapi import APIRouter, Query

from app.services.retrieval import search_documents


router = APIRouter()


@router.get("/search")
def semantic_search(
    query: str = Query(...),
    limit: int = 5,
):
    results = search_documents(
        query=query,
        limit=limit,
    )

    return [
        {
            "content": document.page_content,
            "score": score,
            "document_id": document.metadata["document_id"],
            "file_name": document.metadata["file_name"],
            "page": document.metadata["page"],
            "chunk_index": document.metadata["chunk_index"],
        }
        for document, score in results
    ]