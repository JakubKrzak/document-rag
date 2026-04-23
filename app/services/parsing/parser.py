from docling.document_converter import DocumentConverter
import asyncio
from pathlib import Path

async def parsed_file_content(file_path: Path):
    file_converter = DocumentConverter()
    result = await asyncio.to_thread(file_converter.convert, file_path)
    doc = result.document
    return doc