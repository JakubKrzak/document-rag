from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import models


async def find_file_by_id(file_id: str, db: AsyncSession):
    result = await db.execute(select(models.File).where(models.File.id == file_id))
    return result.scalar_one_or_none()

async def update_file_status(file_id: str, status: models.FileStatus, db: AsyncSession):
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

    file = await find_file_by_id(file_id, db)
    file.status = status
    await db.commit()
    await db.refresh(file)
    return True