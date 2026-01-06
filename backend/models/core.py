from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class APIError(BaseModel):
    message: str
    type: str = "api_error"
    details: Optional[List[Dict]] = None