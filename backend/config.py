import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    duffel_api_key: str = os.getenv("DUFFEL_API_KEY", "")
    duffel_api_version: str = os.getenv("DUFFEL_API_VERSION", "v2")
    duffel_base_url: str = "https://api.duffel.com"
    duffel_timeout: int = 30
    api_client_secret: str = os.getenv("API_CLIENT_SECRET", "")

settings = Settings()