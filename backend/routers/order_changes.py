from fastapi import APIRouter
from backend.services.duffel_client import DuffelClient
from backend.utils.error_handlers import api_exception

router = APIRouter()
duffel = DuffelClient()

@router.post("/order-changes/requests")
async def create_order_change_request(order_id: str, slices: dict):
    try:
        result = await duffel.post("/air/order_change_requests", {"order_id": order_id, "slices": slices})
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)

@router.get("/order-changes/offers")
async def list_order_change_offers(order_change_request_id: str, sort: str = None):
    try:
        params = {"order_change_request_id": order_change_request_id, "sort": sort}
        result = await duffel.get("/air/order_change_offers", params)
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)

@router.get("/order-changes/offers/{offer_id}")
async def get_order_change_offer(offer_id: str):
    try:
        result = await duffel.get(f"/air/order_change_offers/{offer_id}")
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)

@router.post("/order-changes")
async def create_pending_order_change(selected_order_change_offer: dict):
    try:
        result = await duffel.post("/air/order_changes", {"selected_order_change_offer": selected_order_change_offer})
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)

@router.post("/order-changes/{id}/actions/confirm")
async def confirm_order_change(id: str, payment: dict):
    try:
        result = await duffel.post(f"/air/order_changes/{id}/actions/confirm", {"payment": payment})
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)