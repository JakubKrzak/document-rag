import asyncio
import shutil
from sqlalchemy.orm import Session
from database import models
from utils import hash_file_content

def check_file_exists(file_content: bytes, db: Session):
    """

    Function for hash file content and check if file exists in db
    return check file, and file hash

    """

    file_content_hash = hash_file_content.hash_file_content(file_content)
    file_exists = db.query(models.File).filter(models.File.hashed_content == file_content_hash).first()
    return file_exists, file_content_hash


async def save_file_on_disc(file_object, file_content_hash):
    """
    
    Function saves file on disc and return file_path

    """
    name, ext = file_object.filename.rsplit(".", 1)
    file_path = f"disc/{name}_{file_content_hash[:8]}.{ext}"

    file_object.file.seek(0)
    with open(file_path, "wb") as b:
        await asyncio.to_thread(shutil.copyfileobj, file_object.file, b)
    
    return file_path


def add_file_to_database(file_name: str,
                         file_content_hash: str,
                         file_size: int,
                         file_content_type: str,
                         parsed_file_path: str,
                         file_path: str,
                         pages: int,
                         db: Session):
    
    """
    
    Function add file info to db

    """

    add_new_file_info = models.File(file_name=file_name,
                           hashed_content=file_content_hash,
                           file_size=file_size,
                           file_type=file_content_type,
                           parsed_file_path=parsed_file_path,
                           file_path=file_path,
                           pages=pages)
    
    db.add(add_new_file_info)
    db.commit()
    db.refresh(add_new_file_info)

    return add_new_file_info