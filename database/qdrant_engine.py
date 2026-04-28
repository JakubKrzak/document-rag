from qdrant_client import AsyncQdrantClient
from config.settings import settings

qdrant_client = AsyncQdrantClient(
    host=settings.qdrant_host,
    port=settings.qdrant_port
)