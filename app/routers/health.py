from fastapi import APIRouter
from app.storage.vector_store import get_qdrant_client

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check():
    try:
        client = get_qdrant_client()
        collections = client.get_collections()

        return {
            "status": "ok",
            "vector_store": "ok",
            "collections": [c.name for c in collections.collections],
        }

    except Exception as e:
        return {
            "status": "error",
            "vector_store": "error",
            "detail": str(e),
        }
