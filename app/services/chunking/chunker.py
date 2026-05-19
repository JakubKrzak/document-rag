from docling.datamodel.document import DoclingDocument
from docling_core.transforms.chunker import BaseChunker
from docling.chunking import HybridChunker
import asyncio

async def chunk_document(parsed_document: DoclingDocument) -> list[BaseChunker]:
    if not parsed_document:
        return None
    
    
    chunker = HybridChunker(max_tokens=3212)
    chunks = await asyncio.to_thread(
        lambda: list(chunker.chunk(parsed_document))
    )
    return chunks