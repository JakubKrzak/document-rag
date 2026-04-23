from docling_core.transforms.chunker import BaseChunker
import asyncio
import json
from pathlib import Path

async def save_chunks_on_disc(chunks: list[BaseChunker]):
    """
    
    Function saves chunked file on disc
    each chunk is saved as jsonl format
    
    Args:
        chunks: list of chunked file

    """
    if not chunks:
        return 
    
    def _save(chunks: list[BaseChunker]) -> Path:
        name = Path(chunks[0].meta.origin.filename)
        path = f"chunks_disc/{name.stem}.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for chunk in chunks:
                f.write(json.dumps(chunk.model_dump(), ensure_ascii=False) + "\n")
        return path

    chunks_file_path = await asyncio.to_thread(_save, chunks)
    return chunks_file_path