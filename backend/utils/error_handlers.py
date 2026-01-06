from fastapi.responses import JSONResponse
from typing import Any, Dict

def api_exception(error: Exception, status: int = 500) -> JSONResponse:
    """
    Converts any exception into a structured API error response.
    """
    content = {
        "success": False,
        "error": {
            "message": str(error),
            "type": getattr(error, "type", "server_error"),
            "details": getattr(error, "details", None),
        }
    }
    return JSONResponse(status_code=status, content=content)

def validation_error(message: str, details: Any = None, status: int = 422) -> JSONResponse:
    """
    Returns a JSONResponse for validation errors.
    """
    content = {
        "success": False,
        "error": {
            "message": message,
            "type": "validation_error",
            "details": details,
        }
    }
    return JSONResponse(status_code=status, content=content) 