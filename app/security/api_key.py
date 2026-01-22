from fastapi import Header, HTTPException, status
from app.config.settings import settings

def validate_api_key(x_api_key: str | None = Header(default=None)):
    if not x_api_key or x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )