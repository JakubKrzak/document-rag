from sqlalchemy.orm import Session
from database import models
import os

def delete_file_from_db(file_object: models.File, db: Session):
    db.delete(file_object)
    db.commit()

def delete_file_from_disc(file_object: models.File):
    if os.path.exists(file_object.file_path):
        os.remove(file_object.file_path)