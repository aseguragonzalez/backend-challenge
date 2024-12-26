from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from src.infrastructure.ports.api.dependencies import settings
from src.infrastructure.ports.api.settings import Settings


api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)


def api_key(
    api_key_header: str = Security(api_key_header),
    settings: Settings = Depends(settings),
) -> None:
    if api_key_header in settings.api_keys.split(";"):
        return None
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
