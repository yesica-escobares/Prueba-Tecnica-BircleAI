from pydantic import BaseModel
from typing import List


class IngestResponse(BaseModel):
    ingested: int
    skipped: int
    errors: List[str]
