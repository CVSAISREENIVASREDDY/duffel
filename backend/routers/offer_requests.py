from fastapi import APIRouter, Query
from models.duffel import OfferCreateRequest
from services.duffel_client import DuffelClient
from utils.error_handlers import api_exception

router = APIRouter()
duffel = DuffelClient()

@router.post("/offer-requests")
async def create_offer_request(request: OfferCreateRequest):
    try:
        result = await duffel.post("/air/offer_requests", {"data": request.dict(exclude_unset=True)})
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)

@router.get("/offer-requests")
async def list_offer_requests(limit: int = Query(50, ge=1, le=100)):
    try:
        result = await duffel.get("/air/offer_requests", {"limit": limit})
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)

@router.get("/offer-requests/{request_id}")
async def get_offer_request(request_id: str):
    try:
        result = await duffel.get(f"/air/offer_requests/{request_id}")
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e) 