from docling.document_converter import DocumentConverter
import asyncio
from pathlib import Path

from app.services.shared.errors import PathNotFoundError

async def parsed_file_content(file_path: Path):
    if not file_path:
        raise PathNotFoundError(path=file_path)
    
    
    file_converter = DocumentConverter()
    result = await asyncio.to_thread(file_converter.convert, file_path)
    doc = result.document
    
    return doc