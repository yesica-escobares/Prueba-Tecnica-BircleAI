import json

from qdrant_client.http import models
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

from app.config.settings import settings
from app.storage.vector_store import get_qdrant_client


def _filter_eq(key: str, value: str) -> Filter:
    return Filter(
        must=[
            FieldCondition(
                key=key,
                match=MatchValue(value=value),
            )
        ]
    )


def delete_document_by_doc_id(doc_id: str) -> int:
    """
    Deletes all chunks associated with a document.

    "doc_id" can be:

    - the actual document ID (doc_id/ref_doc_id/document_id in Qdrant), or
    - the filename (if provided by the client), or
    - an ID that remains within _node_content (fallback).
    """
    client = get_qdrant_client()

    # First attempt: delete by indexable fields of the payload
    for key in (
        "doc_id",
        "ref_doc_id",
        "document_id",
        "filename",
        "metadata.doc_id", 
    ):
        query_filter = _filter_eq(key, doc_id)

        cnt = client.count(
            collection_name=settings.QDRANT_COLLECTION,
            count_filter=query_filter,
            exact=True,
        ).count

        if cnt > 0:
            client.delete(
                collection_name=settings.QDRANT_COLLECTION,
                points_selector=models.FilterSelector(filter=query_filter),
                wait=True,
            )
            return cnt

    # Second attempt: if the doc_id is inside "_node_content" (JSON) and not as an indexable field
    point_ids: list = []
    next_offset = None

    while True:
        points, next_offset = client.scroll(
            collection_name=settings.QDRANT_COLLECTION,
            limit=256,
            offset=next_offset,
            with_payload=True,
            with_vectors=False,
        )

        for p in points:
            payload = getattr(p, "payload", None) or {}
            node_content = payload.get("_node_content")
            if not node_content:
                continue

            try:
                meta = json.loads(node_content).get("metadata", {})
            except Exception:
                continue

            if meta.get("doc_id") == doc_id:
                point_ids.append(p.id)

        if next_offset is None:
            break

    if point_ids:
        client.delete(
            collection_name=settings.QDRANT_COLLECTION,
            points_selector=models.PointIdsList(points=point_ids),
            wait=True,
        )
        return len(point_ids)

    return 0
