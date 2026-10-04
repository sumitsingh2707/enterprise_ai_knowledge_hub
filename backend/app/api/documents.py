from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Query
from sqlalchemy.orm import Session
from pathlib import Path
from app.core.database import get_db
from app.models.document import Document
from app.schemas.documents import DocumentResponse
from app.services.rag_ingestion import ingest_document
from app.services.document_service import (
    save_file,
    validate_file,
)
from app.services.job_service import (
    enqueue_document_processing,
)

router = APIRouter()


# ---------------------------------------------------------
# Upload document
# ---------------------------------------------------------

@router.post("/documents", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    document = None
    job_id = None

    try:

        # ---------------------------------------------
        # 1. Validate file
        # ---------------------------------------------

        extension = validate_file(file)

        # ---------------------------------------------
        # 2. Save physical file
        # ---------------------------------------------

        file_path, file_size = save_file(
            file,
            extension,
        )

        # ---------------------------------------------
        # 3. Create database record
        # ---------------------------------------------

        document = Document(
            file_name=file.filename,
            file_type=extension.replace(
                ".",
                "",
            ).upper(),
            mime_type=(
                file.content_type
                or "application/octet-stream"
            ),
            file_path=file_path,
            file_size=file_size,
            status="PROCESSING",
            uploaded_by=1,
        )

        db.add(document)

        db.commit()

        db.refresh(document)

        # ---------------------------------------------
        # 4. Queue background processing
        # ---------------------------------------------

        print("Document ready for queue")

        job_id = enqueue_document_processing(
            document.id
        )

        print(
            f"Document queued. Job ID: {job_id}"
        )

    except Exception as exc:

        # ---------------------------------------------
        # Handle upload / queue failure
        # ---------------------------------------------

        if document:

            document.status = "FAILED"
            document.error_message = str(exc)

            db.commit()
            db.refresh(document)

        raise

    # ---------------------------------------------
    # 5. Return immediately
    # ---------------------------------------------

    return {
        "id": document.id,
        "file_name": document.file_name,
        "file_type": document.file_type,
        "mime_type": document.mime_type,
        "file_size": document.file_size,
        "status": document.status,
        "error_message": document.error_message,
        "uploaded_by": document.uploaded_by,
        "created_at": document.created_at,
        "updated_at": document.updated_at,
        "job_id": job_id,
    }



@router.get(
    "/documents",
    response_model=list[DocumentResponse],
)
def list_documents(
    db: Session = Depends(get_db),
):
    return db.query(Document).order_by(Document.created_at.desc()).all()


@router.get(
    "/documents/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return document


@router.delete("/documents/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    file_path = Path(document.file_path)

    if file_path.exists():
        file_path.unlink()

    # db.delete(document)
    document = db.query(Document).order_by(Document.created_at.desc()).all()
    db.delete_all(document)
    db.commit()

    return {"message": "Document deleted successfully"}


@router.get(
    "/documents",
    response_model=list[DocumentResponse],
)
def list_documents(
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Document)

    if search:
        query = query.filter(Document.file_name.ilike(f"%{search}%"))

    return query.order_by(Document.created_at.desc()).all()



@router.get("/{document_id}/status")
def get_document_status(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return {
        "id": document.id,
        "file_name": document.file_name,
        "status": document.status,
        "error_message": document.error_message,
    }
