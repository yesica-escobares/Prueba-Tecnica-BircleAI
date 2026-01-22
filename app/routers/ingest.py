from fastapi import APIRouter, UploadFile, File, Depends
import shutil

from app.security.api_key import validate_api_key
from app.config.settings import settings
from app.services.ingest_service import ingest_directory
from app.schemas.ingest import IngestResponse


router = APIRouter(
    prefix="/ingest",
    tags=["ingest"],
    dependencies=[Depends(validate_api_key)],
)


@router.post("")
async def ingest_files(files: list[UploadFile] = File(...)):
    data_dir = settings.DATA_DIR
    data_dir.mkdir(parents=True, exist_ok=True)  

    ingested = 0
    skipped = 0
    errors = []

    for file in files:
        try:
            file_path = data_dir / file.filename

            # Avoid overwriting
            if file_path.exists():
                skipped += 1
                continue

            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)  

            ingested += 1

        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")

    # Reindex only if there were new files
    if ingested > 0:
        ingest_directory(data_dir)

    return IngestResponse(
        ingested=ingested,
        skipped=skipped,
        errors=errors,
    )
