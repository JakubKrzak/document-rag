from database import qdrant_client
from qdrant_client.models import VectorParams, Distance, PointStruct

async def check_collection_exists(collection_name: str):
    return await qdrant_client.collection_exists(collection_name=collection_name)


async def create_collection(collection_name: str, vector_dim: int):
    try:
        await qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_dim,
                distance=Distance.COSINE
        ))
        return print(f"Collection: {collection_name} created")
    except Exception as e:
        print(e)



async def upser_points(points, collection_name):
    if not await check_collection_exists(collection_name=collection_name):
        raise Exception(f"Collection: {collection_name} not exists")

    qdrant_points = []
    for index, point in enumerate(points):
        qdrant_point = PointStruct(
            id=index,
            vector=point["vector"],
            payload=point["payload"]
        )

        qdrant_points.append(qdrant_point)
        
    try:
        await qdrant_client.upsert(
            collection_name=collection_name,
            points=qdrant_points
        )
    except Exception as e:
        raise Exception(f"{e}")