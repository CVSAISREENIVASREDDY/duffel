from fastapi import APIRouter, Depends, Query
from services.duffel_client import DuffelClient
from utils.error_handlers import api_exception

router = APIRouter()
duffel = DuffelClient()

@router.get("/offers")
async def list_offers(offer_request_id: str = Query(...), limit: int = 50, sort: str = None):
    try:
        params = {"offer_request_id": offer_request_id, "limit": limit, "sort": sort}
        result = await duffel.get("/air/offers", params)
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)

@router.get("/offers/{offer_id}")
async def get_offer(offer_id: str):
    try:
        result = await duffel.get(f"/air/offers/{offer_id}")
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)