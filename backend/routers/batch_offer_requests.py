from fastapi import APIRouter
from services.duffel_client import DuffelClient
from utils.error_handlers import api_exception

router = APIRouter()
duffel = DuffelClient()

@router.post("/batch-offer-requests")
async def create_batch_offer_request(data: dict):
    try:
        result = await duffel.post("/air/batch_offer_requests", data)
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)

@router.get("/batch-offer-requests/{id}")
async def get_batch_offer_request(id: str):
    try:
        result = await duffel.get(f"/air/batch_offer_requests/{id}")
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)