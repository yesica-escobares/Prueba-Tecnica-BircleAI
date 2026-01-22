from llama_index.core import VectorStoreIndex
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever

from app.storage.vector_store import get_vector_store
from app.services.llm import get_llm


def get_query_engine(
    top_k: int,
    filters: dict | None = None,
    streaming: bool = False,
):
    storage_context = get_vector_store()

    index = VectorStoreIndex.from_vector_store(
        storage_context.vector_store
    )

    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=top_k,
        filters=filters,
    )

    llm = get_llm(streaming=streaming)

    return RetrieverQueryEngine.from_args(
        retriever=retriever,
        llm=llm,
        response_mode="compact",
        streaming=streaming,
    )


def run_query(q: str, top_k: int, filters: dict | None = None):
    query_engine = get_query_engine(top_k, filters, streaming=False)

    response = query_engine.query(q)

    return response


def stream_query(q: str, top_k: int, filters: dict | None = None):
    query_engine = get_query_engine(top_k, filters, streaming=True)
    
    response = query_engine.query(q)
    
    return response



def extract_sources(response) -> list[dict]:
    sources = []

    for node in response.source_nodes:
        metadata = node.node.metadata

        sources.append({
            "doc_id": (
                getattr(node, "ref_doc_id", None)
                or metadata.get("ref_doc_id")
                or metadata.get("document_id")
                or getattr(node, "document_id", None)
                or metadata.get("doc_id")
            ),#metadata.get("doc_id"),
            "filename": metadata.get("filename"),
            "page": metadata.get("page"),
            "score": float(node.score),
            "snippet": node.node.text[:300],
        })

    return sources
