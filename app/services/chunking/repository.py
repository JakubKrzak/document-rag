
from docling_core.transforms.chunker import BaseChunker
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.file_services import find_file_by_id

async def add_chunked_info_to_db(file_id: int, chunks: list[BaseChunker], chunks_file_path: Path, db: AsyncSession):
    file = await find_file_by_id(file_id, db)
    file.chunks_path = chunks_file_path
    file.chunks_number = len(chunks)
    await db.commit()
    await db.refresh(file)
    return True