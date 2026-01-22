from pathlib import Path
from app.config.settings import settings
from app.storage.vector_store import get_qdrant_client


def get_stats():
    client = get_qdrant_client()

    # Local storage disk size
    db_path = Path(settings.VECTOR_DB_PATH)
    size_bytes = sum(f.stat().st_size for f in db_path.rglob("*") if f.is_file())

    try:
        # If the collection does not yet exist, return empty.
        if hasattr(client, "collection_exists") and not client.collection_exists(settings.QDRANT_COLLECTION):
            return {"documents": 0, "chunks": 0, "last_ingest": "", "collection_size_mb": round(size_bytes / (1024 * 1024), 2)}

        info = client.get_collection(settings.QDRANT_COLLECTION)

        chunks = info.points_count or 0

        # Count documents and last ingestion reading payload
        filenames = set()
        
        last_ingest = ""
        offset = None

        while True:
            points, offset = client.scroll(
                collection_name=settings.QDRANT_COLLECTION,
                limit=256,
                offset=offset,
                with_payload=["filename", "ingest_timestamp"],
                with_vectors=False,
            )

            for p in points:
                payload = getattr(p, "payload", None) or {}
                fn = payload.get("filename")
                if fn:
                    filenames.add(fn)

                ts = payload.get("ingest_timestamp")
                if ts and ts > last_ingest:
                    last_ingest = ts

            if offset is None:
                break

        return {
            "documents": len(filenames),
            "chunks": chunks,
            "last_ingest": last_ingest,
            "collection_size_mb": round(size_bytes / (1024 * 1024), 2),
        }

    except Exception:
        return {
            "documents": 0,
            "chunks": 0,
            "last_ingest": "",
            "collection_size_mb": round(size_bytes / (1024 * 1024), 2),
        }
