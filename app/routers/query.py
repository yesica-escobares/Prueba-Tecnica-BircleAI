from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse

from app.security.api_key import validate_api_key
from app.schemas.query import QueryRequest, QueryResponse
from app.services.query_service import run_query, stream_query, extract_sources
from app.services.streaming import sse_event_generator
from app.security.rate_limit import limiter

router = APIRouter(prefix="/query", tags=["query"],  dependencies=[Depends(validate_api_key)])

@router.post("", response_model=QueryResponse)
@limiter.limit("5/minute")
def query_documents(request: Request,req: QueryRequest):

    # Streaming 
    if req.stream:
        response = stream_query(
            q=req.q,
            top_k=req.top_k,
            filters=req.filters,
        )

        return StreamingResponse(
            sse_event_generator(response),
            media_type="text/event-stream",
        )

    # No streaming 
    response = run_query(
        q=req.q,
        top_k=req.top_k,
        filters=req.filters,
    )

    sources = extract_sources(response)

    if not sources:
        return QueryResponse(
            answer="No se encontró contexto relevante para responder la pregunta.",
            sources=[],
            retrieval_params={
                "top_k": req.top_k,
                "filters": req.filters,
            },
        )

    return QueryResponse(
        answer=str(response),
        sources=sources,
        retrieval_params={
            "top_k": req.top_k,
            "filters": req.filters,
        },
    )

