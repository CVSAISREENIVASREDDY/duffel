from fastapi import Request, HTTPException, Depends
from config import settings

async def verify_api_key(request: Request):
    api_key = request.headers.get("x-api-key")
    if not api_key or api_key != settings.api_client_secret:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing API Key") 