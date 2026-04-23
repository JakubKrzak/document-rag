from app.services import file_chunk
import json
from FlagEmbedding import BGEM3FlagModel
from pathlib import Path
from docling_core.transforms.chunker import BaseChunker
import asyncio
_model = None

def get_model():
    global _model
    if _model is None:
        _model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=False)
    return _model

def load_chunks_from_disk(path: Path) -> list[BaseChunker]:
    chunks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            chunk = json.loads(line)
            chunks.append(chunk)
    
    return chunks

async def embed_chunk(chunk) -> list[float]:
    chunk_text = chunk["text"]
    vectors = await asyncio.to_thread(
        get_model().encode,
        sentences=chunk_text,
        batch_size=10,
        max_length=8000,
        return_dense=True
    )

    return vectors["dense_vecs"]

def create_point(chunk, vectors: list[float], number: int) -> dict:

    page_number = chunk['meta']["doc_items"][0]['prov'][0]["page_no"]
    chunk_file_name = chunk["meta"]['origin']['filename']
    mimetype = chunk["meta"]['origin']['mimetype']
    label = chunk['meta']["doc_items"][0]["label"]

    point_name = f"{Path(chunk_file_name).stem}_chunk_{number}"

    point = {}
    point["vector"] = vectors.tolist()
    point["payload"] = {"text": chunk["text"],
                        "file_name": chunk_file_name,
                        "point_name": point_name,
                        "page": page_number,
                        "mime_type": mimetype,
                        "label": label.value}
                        
    return point

async def build_point(chunks: list[dict]) -> list[dict]:
    points = []
    for i, chunk in enumerate(chunks):
        vectors = await embed_chunk(chunk)
        point = create_point(chunk, vectors, i)
        points.append(point)
    
    return points

async def save_points_on_disk(points: list[dict]):
    name = Path(points[0]["payload"]["file_name"])
    path = f"embed_disk/{name.stem}.jsonl"

    def _write(points, path):
        with open(path, "w", encoding="utf-8") as f:
            for point in points:
                f.write(json.dumps(point, ensure_ascii=False) + "\n")

    await asyncio.to_thread(_write, points, path) 
    return path