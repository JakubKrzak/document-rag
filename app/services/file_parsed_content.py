from docling.document_converter import DocumentConverter
import asyncio
from pathlib import Path

async def parsed_file_content(file_path: Path):
    file_converter = DocumentConverter()
    result = await asyncio.to_thread(file_converter.convert, file_path)
    doc = result.document
    return doc

async def save_parsed_file_on_disc(parsed_file: object):
    file_path = f"parsed_disc/{parsed_file.name}.md"
    
    def _write():
        md = parsed_file.export_to_markdown()
        with open(file_path, "w") as f:
            f.write(md)
    await asyncio.to_thread(_write)

    return file_path