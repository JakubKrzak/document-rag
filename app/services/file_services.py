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