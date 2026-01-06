from fastapi import APIRouter
from backend.services.duffel_client import DuffelClient
from backend.utils.error_handlers import api_exception

router = APIRouter()
duffel = DuffelClient()

@router.post("/partial-offer-requests")
async def create_partial_offer_request(data: dict):
    try:
        result = await duffel.post("/air/partial_offer_requests", data)
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)

@router.get("/partial-offer-requests/{id}")
async def get_partial_offer_request(id: str, selected_partial_offer: list = None):
    try:
        params = {'selected_partial_offer[]': selected_partial_offer}
        result = await duffel.get(f"/air/partial_offer_requests/{id}", params)
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)

@router.get("/partial-offer-requests/{id}/fares")
async def get_full_offer_fares(id: str, selected_partial_offer: list = None):
    try:
        params = {'selected_partial_offer[]': selected_partial_offer}
        result = await duffel.get(f"/air/partial_offer_requests/{id}/fares", params)
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)