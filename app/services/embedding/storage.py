import json
from pathlib import Path
from docling_core.transforms.chunker import BaseChunker
import asyncio

def load_chunks_from_disk(path: Path) -> list[BaseChunker]:
    chunks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            chunk = json.loads(line)
            chunks.append(chunk)
    
    return chunks

async def save_points_on_disk(points: list[dict]):
    name = Path(points[0]["payload"]["file_name"])
    path = f"embed_disk/{name.stem}.jsonl"

    def _write(points, path):
        with open(path, "w", encoding="utf-8") as f:
            for point in points:
                f.write(json.dumps(point, ensure_ascii=False) + "\n")

    await asyncio.to_thread(_write, points, path) 
    return path