from fastapi import APIRouter, Query
from backend.services.duffel_client import DuffelClient
from backend.utils.error_handlers import api_exception

router = APIRouter()
duffel = DuffelClient()

@router.get("/seat-maps")
async def get_seat_maps(offer_id: str = Query(...)):
    try:
        result = await duffel.get("/air/seat_maps", {"offer_id": offer_id})
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e) 