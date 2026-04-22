from app.services import file_chunk
import json
from FlagEmbedding import BGEM3FlagModel
from pathlib import Path
from docling_core.transforms.chunker import BaseChunker

model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=False)

def load_chunks_from_disc(path: Path) -> list[BaseChunker]:
    chunks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            chunk = json.loads(line)
            chunks.append(chunk)
    
    return chunks

def embedding_model(chunk: str) -> list[float]:
    chunk_text = chunk["text"]
    vectors = model.encode(sentences=chunk_text,
                           batch_size=10,
                           max_length=8000,
                           return_dense=True)
    return vectors["dense_vecs"]

def create_point(chunk, vectors: list[float], number: int) -> dict:

    page_number = chunk['meta']["doc_items"][0]['prov'][0]["page_no"]
    chunk_file_name = chunk["meta"]['origin']['filename']
    mimetype = chunk["meta"]['origin']['mimetype']
    label = chunk['meta']["doc_items"][0]["label"]

    point_name = f"{Path(chunk_file_name).stem}_chunk_{number}"

    point = {}
    point["vector"] = vectors
    point["payload"] = {"text": chunk["text"],
                        "file_name": chunk_file_name,
                        "point_name": point_name,
                        "page": page_number,
                        "mime_type": mimetype,
                        "label": label}
                        
    return point

def embedded_chunks(path: Path) -> list[dict]:
    chunks = load_chunks_from_disc(path=path)
    embedded_finish = []
    for i, chunk in enumerate(chunks):
        vectors = embedding_model(chunk)
        point = create_point(chunk, vectors, i)
        embedded_finish.append(point)
    
    return embedded_finish