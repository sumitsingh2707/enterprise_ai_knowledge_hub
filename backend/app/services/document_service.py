from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

UPLOAD_DIR = Path("uploads")

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


def validate_file(file: UploadFile) -> str:
    if not file.filename:
        raise ValueError("File name is required")
    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type {extension}")
    return extension


def save_file(file: UploadFile, extension: str) -> tuple[str, int]:
    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )
    generated_name= f"{uuid4()}{extension}"
    file_path=UPLOAD_DIR/generated_name
    file.file.seek(0)
    content =  file.file.read()
    file_path.write_bytes(content)
    return str(file_path), len(content)