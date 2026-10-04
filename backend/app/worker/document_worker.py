from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.document import Document
from app.services.rag_ingestion import ingest_document


engine = create_engine(
    settings.database_url
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def process_document(
    document_id: int,
):
    db = SessionLocal()

    try:
        # -----------------------------------------
        # 1. Find document
        # -----------------------------------------
        print("did it come here document")

        document = (
            db.query(Document)
            .filter(
                Document.id == document_id
            )
            .first()
        )

        if not document:
            raise ValueError(
                f"Document {document_id} not found"
            )

        # -----------------------------------------
        # 2. Mark as PROCESSING
        # -----------------------------------------

        document.status = "PROCESSING"

        db.commit()

        # -----------------------------------------
        # 3. Run RAG ingestion
        # -----------------------------------------

        ingest_document(
            file_path=document.file_path,
            file_type=document.file_type,
            document_id=document.id,
            file_name=document.file_name,
        )
        print("ingest document")

        # -----------------------------------------
        # 4. Mark as READY
        # -----------------------------------------

        document.status = "READY"
        document.error_message = None

        db.commit()

        return {
            "document_id": document.id,
            "status": "READY",
        }

    except Exception as exc:

        # -----------------------------------------
        # 5. Mark as FAILED
        # -----------------------------------------

        document.status = "FAILED"
        document.error_message = str(exc)

        db.commit()

        raise

    finally:
        db.close()
