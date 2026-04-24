import datetime
from uuid import UUID
from pydantic import BaseModel
from database.models import FileStatus
from typing import Optional

class FileResponse(BaseModel):
    id: UUID
    file_name: str
    hashed_content: str
    file_size: int
    file_type: str
    parsed_file_path: Optional[str]=None
    file_path: str
    pages: Optional[int]=None
    uploaded_at: datetime
    chunks_path: Optional[str]=None
    chunks_number: Optional[int]=None
    embed_path: Optional[str]=None
    vectors_dim: Optional[int]=None
    status: FileStatus

    class Config:
        from_attributes = True
        arbitrary_types_allowed=True