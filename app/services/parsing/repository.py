from sqlalchemy.ext.asyncio import AsyncSession
from app.services.shared import find_file_by_id

async def add_parsed_info_to_db(file_id: str, parsed_file_path: str, pages: int, db: AsyncSession):
    file = await find_file_by_id(file_id, db)
    file.parsed_file_path = parsed_file_path
    file.pages = pages
    await db.commit()
    await db.refresh(file)
    return True