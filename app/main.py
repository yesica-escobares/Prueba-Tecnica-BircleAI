from fastapi import FastAPI
import logging
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse
from llama_index.core import Settings

from app.config.settings import settings
from app.services.ingest_service import ingest_directory
from app.routers.ingest import router as ingest_router
from app.routers.query import router as query_router
from app.routers.health import router as health_router
from app.routers.stats import router as stats_router
from app.config.logging import setup_logging
from app.middleware.logging import LoggingMiddleware
#from app.security.rate_limit import limiter
from app.routers.documents import router as documents_router
from app.routers.query import limiter
from app.services.llm import get_llm
from app.services.embeddings import get_embedding_model
from app.storage.vector_store import get_qdrant_client


Settings.llm = get_llm()
Settings.embed_model = get_embedding_model()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG API")

def _collection_has_points() -> bool:
    client = get_qdrant_client()
    
    try:
        if hasattr(client, "collection_exists") and not client.collection_exists(settings.QDRANT_COLLECTION):
            return False
        info = client.get_collection(settings.QDRANT_COLLECTION)
        return (info.points_count or 0) > 0
    
    except Exception:
        return False

@app.on_event("startup")
def startup_event():
    settings.DATA_DIR.mkdir(exist_ok=True)

    if _collection_has_points():
        logger.info(
            "Skipping initial ingest: the collection already contains data",
            extra={"collection": settings.QDRANT_COLLECTION},
        )
        return

    ingested = ingest_directory(settings.DATA_DIR)
    logger.info(
        "Initial intake completed",
        extra={"documents_ingested": ingested},
    )
    


app.include_router(ingest_router)
app.include_router(query_router)
app.include_router(health_router)
app.include_router(stats_router)
app.include_router(documents_router)


setup_logging()
app.add_middleware(LoggingMiddleware)



app.state.limiter = limiter
#app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
    )
