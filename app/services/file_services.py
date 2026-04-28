from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import models
from ..schemas import schemas_file

async def find_file_by_id(file_id: str, db: AsyncSession):
    result = await db.execute(select(models.File).where(models.File.id == file_id))
    return result.scalar_one_or_none()

async def find_file_by_name(file_name: str, db: AsyncSession):
    result = await db.execute(select(models.File).where(models.File.file_name == file_name))
    return result.scalars().all()

async def get_all_files(db: AsyncSession) -> list[schemas_file.FileResponse]:
    result = await db.execute(select(models.File))
    return result.scalars().all()

async def check_file_status(file_id: str, status: models.FileStatus, db: AsyncSession):
    file = await find_file_by_id(file_id=file_id, db=db)

    if file is None:
        return None

    return file.status == status 

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

async def add_parsed_info_to_db(file_id: str, parsed_file_path: str, pages: int, db: AsyncSession):
    file = await find_file_by_id(file_id, db)
    file.parsed_file_path = parsed_file_path
    file.pages = pages
    await db.commit()
    await db.refresh(file)
    return True

async def add_embed_info_to_db(file_id: str, embed_path: str, vectors_dim: int, db: AsyncSession):
    file = await find_file_by_id(file_id=file_id, db=db)
    file.embed_path = embed_path
    file.vectors_dim = vectors_dim
    await db.commit()
    await db.refresh(file)
    return True