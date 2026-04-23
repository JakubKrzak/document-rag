from .model import get_model
from pathlib import Path
import asyncio

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