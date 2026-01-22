from fastapi import APIRouter, Depends, HTTPException, status

from app.security.api_key import validate_api_key
from app.services.delete_service import delete_document_by_doc_id

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
    dependencies=[Depends(validate_api_key)],
)


@router.delete("/{doc_id}")
def delete_document(doc_id: str):
    deleted = delete_document_by_doc_id(doc_id)

    if deleted == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return {
        "doc_id": doc_id,
        "deleted_chunks": deleted,
        "status": "deleted",
    }
