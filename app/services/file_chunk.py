

from docling.datamodel.document import DoclingDocument
from docling_core.transforms.chunker import BaseChunker
from docling.chunking import HybridChunker
import asyncio
import json
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.file_services import find_file_by_id

async def chunk_document(parsed_document: DoclingDocument) -> list[BaseChunker]:
    if not parsed_document:
        return None
    
    chunker = HybridChunker(max_tokens=3212)
    chunks = await asyncio.to_thread(
        lambda: list(chunker.chunk(parsed_document))
    )
    return chunks

async def save_chunks_on_disc(chunks: list[BaseChunker]):
    """
    
    Function saves chunked file on disc
    each chunk is saved as jsonl format
    
    Args:
        chunks: list of chunked file

    """
    if not chunks:
        return 
    
    def save_(chunks: list[BaseChunker]) -> Path:
        name = Path(chunks[0].meta.origin.filename)
        path = f"chunks_disc/{name.stem}.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for chunk in chunks:
                f.write(json.dumps(chunk.model_dump(), ensure_ascii=False) + "\n")
        return path

    chunks_file_path = await asyncio.to_thread(save_, chunks)
    return chunks_file_path


async def add_chunked_info_to_db(file_id: int, chunks: list[BaseChunker], chunks_file_path: Path, db: AsyncSession):
    file = await find_file_by_id(file_id, db)
    file.chunks_path = chunks_file_path
    file.chunks_number = len(chunks)
    await db.commit()
    await db.refresh(file)
    return True