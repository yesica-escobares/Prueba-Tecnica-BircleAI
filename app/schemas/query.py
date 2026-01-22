from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any


class QueryRequest(BaseModel):
    q: str = Field(..., description="Pregunta del usuario")
    top_k: int = Field(5, ge=1, le=20)
    filters: Optional[Dict[str, str]] = None
    stream: bool = False


class SourceChunk(BaseModel):
    doc_id: str
    filename: str
    page: int | None = None
    score: float
    snippet: str


class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
    retrieval_params: Dict[str, Any]