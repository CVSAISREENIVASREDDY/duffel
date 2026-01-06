from fastapi import APIRouter, Query
from backend.services.duffel_client import DuffelClient
from backend.utils.error_handlers import api_exception

router = APIRouter()
duffel = DuffelClient()

@router.post("/airline-credits")
async def create_airline_credit(data: dict):
    try:
        result = await duffel.post("/air/airline_credits", data)
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)

@router.get("/airline-credits")
async def list_airline_credits(user_id: str = None, limit: int = 50):
    try:
        params = {"user_id": user_id, "limit": limit}
        result = await duffel.get("/air/airline_credits", params)
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)

@router.get("/airline-credits/{id}")
async def get_airline_credit(id: str):
    try:
        result = await duffel.get(f"/air/airline_credits/{id}")
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)