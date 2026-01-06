import httpx
from config import settings

class DuffelClient:
    def __init__(self):
        self.base_url = settings.duffel_base_url
        self.timeout = settings.duffel_timeout
        self.headers = {
            "Authorization": f"Bearer {settings.duffel_api_key}",
            "Duffel-Version": settings.duffel_api_version,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    async def get(self, path, params=None):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.get(f"{self.base_url}{path}", headers=self.headers, params=params)
            r.raise_for_status()
            return r.json()

    async def post(self, path, data=None):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.post(f"{self.base_url}{path}", headers=self.headers, json=data or {})
            
            # IMPROVED ERROR HANDLING
            if r.is_error:
                try:
                    # Try to get the real error from Duffel
                    error_details = r.json()
                except:
                    error_details = r.text
                
                try:
                    r.raise_for_status()
                except httpx.HTTPStatusError as e:
                    # Attach the details so api_exception handler can see them
                    e.details = error_details
                    raise e
            
            return r.json()

    async def patch(self, path, data=None):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.patch(f"{self.base_url}{path}", headers=self.headers, json=data or {})
            r.raise_for_status()
            return r.json()

    async def delete(self, path):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.delete(f"{self.base_url}{path}", headers=self.headers)
            r.raise_for_status()
            return r.json()