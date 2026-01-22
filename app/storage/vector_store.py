from qdrant_client import QdrantClient
from llama_index.core import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore

from app.config.settings import settings


_qdrant_client = None
_storage_context = None


def get_qdrant_client() -> QdrantClient:
    global _qdrant_client
    if _qdrant_client is None:
        settings.VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)
        _qdrant_client = QdrantClient(path=str(settings.VECTOR_DB_PATH))
    return _qdrant_client


def get_vector_store() -> StorageContext:
    global _qdrant_client, _storage_context

    if _storage_context is not None:
        return _storage_context


    client = get_qdrant_client()

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=settings.QDRANT_COLLECTION,
    )

    _storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    return _storage_context
