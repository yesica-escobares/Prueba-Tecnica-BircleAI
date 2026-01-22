import uuid
import mimetypes
import os
from datetime import datetime
from pathlib import Path

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

from app.storage.vector_store import get_vector_store


SUPPORTED_EXTENSIONS = [".txt", ".pdf"]



def _build_file_metadata(file_path: str) -> dict:
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "application/octet-stream"

    try:
        size_bytes = os.path.getsize(file_path)
    except OSError:
        size_bytes = None

    return {
        "filename": Path(file_path).name,
        "mime_type": mime_type,
        "size_bytes": size_bytes,
        "ingest_timestamp": datetime.utcnow().isoformat(),
    }


def ingest_directory(data_dir: Path) -> int:

    storage_context = get_vector_store()

    reader = SimpleDirectoryReader(
        input_dir=str(data_dir),
        required_exts=SUPPORTED_EXTENSIONS,
        file_metadata=lambda file_path: _build_file_metadata(str(file_path)),
    )

    documents = reader.load_data()

    if not documents:
        return 0


    VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True,
    )

    return len(documents)
