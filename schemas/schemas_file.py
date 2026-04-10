import datetime
from uuid import UUID
from pydantic import BaseModel

class FileResponse(BaseModel):
    id: UUID
    file_name: str
    hashed_content: str
    file_size: int
    file_type: str
    file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed=True