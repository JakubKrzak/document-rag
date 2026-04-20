import enum

from fastapi import HTTPException
from sqlalchemy.orm import Session
from database import models

from ..schemas import schemas_file

def find_file_by_id(file_id: str, db: Session):
    return db.query(models.File).filter(models.File.id == file_id).first()

def find_file_by_name(file_name: str, db: Session):
    return db.query(models.File).filter(models.File.file_name == file_name).all()

def get_all_files(db: Session) -> list[schemas_file.FileResponse]:
    return db.query(models.File).all()

def check_file_status(id: str, status: models.FileStatus, db: Session):
    file = db.query(models.File).filter(models.File.id == id).first()

    if file is None:
        return False

    return file.status == status


def update_file_status(file_id: str, status: models.FileStatus, db: Session):
    """
    
    Function for update file status, 
    status is enum model, status:
    UPLOADED
    PARSED
    CHUNKED
    EMBEDDED
    COMPLETED

    Args:
        file_id: file id
        status: file status
    
    Returns:
        True if status was changed
    
    """

    file = find_file_by_id(file_id, db)
    file.status = status
    db.commit()

    return True