from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.services.shared.errors import AddFileToDataBaseError
from utils import hash_file_content
from sqlalchemy import select
from database import models

async def check_file_exists(file_content: bytes, db: AsyncSession):
    """

    Function for hash file content and check if file exists in db
    return check file, and file hash

    """

    file_content_hash = hash_file_content.hash_file_content(file_content)
    file = await db.execute(select(models.File).where(models.File.hashed_content == file_content_hash))


    return file.scalar_one_or_none(), file_content_hash

async def add_file_to_database(file_name: str,
                         file_content_hash: str,
                         file_size: int,
                         file_content_type: str,
                         file_path: str,
                         status: models.FileStatus,
                         db: AsyncSession):
    
    """
    
    Function add file info to db

    """

    file = models.File(file_name=file_name,
                           hashed_content=file_content_hash,
                           file_size=file_size,
                           file_type=file_content_type,
                           file_path=file_path,
                           status=models.FileStatus.UPLOADED)

    
    try:
        db.add(file)
        await db.commit()
        await db.refresh(file)
    except SQLAlchemyError:
        await db.rollback()
        raise AddFileToDataBaseError(file_name=file_name)
    
    return file