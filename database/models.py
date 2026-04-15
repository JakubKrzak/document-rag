from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.database_engine import Base
from uuid import uuid4

class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    file_name = Column(String, nullable=False)
    hashed_content = Column(String, unique=True, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String, nullable=False)
    parsed_file_path = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    pages = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.now)
