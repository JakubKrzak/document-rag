

from docling.datamodel.document import DoclingDocument
from docling_core.transforms.chunker import BaseChunker
from docling.chunking import HybridChunker
from app.services.file_parsed_content import parsed_file_content
import asyncio
import json
from pathlib import Path


async def chunk_document(parsed_document: DoclingDocument) -> list[BaseChunker]:
    if not parsed_document:
        return None
    
    chunker = HybridChunker(max_tokens=3212)
    chunks = await asyncio.to_thread(
        lambda: list(chunker.chunk(parsed_document))
    )
    return chunks

def save_chunks_on_disc(chunks: list[BaseChunker]):
    """
    
    Function saves chunked file on disc
    each chunk is saved as jsonl format
    
    Args:
        chunks: list of chunked file

    """
    if not chunks:
        return None
    
    name = Path(chunks[0].meta.origin.filename)
    path = f"chunks_disc/{name.stem}.jsonl"
    with open(path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk.model_dump(), ensure_ascii=False) + "\n")