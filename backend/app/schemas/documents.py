from datetime import datetime
from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: int
    file_name: str
    file_type: str
    mime_type: str
    file_size: int
    status: str
    error_message: str | None
    uploaded_by: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }