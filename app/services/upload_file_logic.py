import asyncio
import shutil
from sqlalchemy.orm import Session
from database import models
from utils import hash_file_content
from app.logger.log_conf import get_logger
logger = get_logger(__name__)

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
    logger.debug(f"file: {file_object.filename} written to {file_path}")
    return file_path



def add_file_to_database(file_name: str,
                         file_content_hash: str,
                         file_size: int,
                         file_content_type: str,
                         file_path: str,
                         status: models.FileStatus,
                         db: Session):
    
    """
    
    Function add file info to db

    """

    file = models.File(file_name=file_name,
                           hashed_content=file_content_hash,
                           file_size=file_size,
                           file_type=file_content_type,
                           file_path=file_path,
                           status=models.FileStatus.UPLOADED)

    
    db.add(file)
    db.commit()
    db.refresh(file)

    return file