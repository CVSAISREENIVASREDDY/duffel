from fastapi import APIRouter
from services.duffel_client import DuffelClient
from utils.error_handlers import api_exception

router = APIRouter()
duffel = DuffelClient()

@router.post("/order-cancellations")
async def create_order_cancellation(order_id: str):
    try:
        result = await duffel.post("/air/order_cancellations", {"order_id": order_id})
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)

@router.get("/order-cancellations")
async def list_order_cancellations(order_id: str = None, limit: int = 50):
    try:
        params = {"order_id": order_id, "limit": limit}
        result = await duffel.get("/air/order_cancellations", params)
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)

@router.get("/order-cancellations/{cancellation_id}")
async def get_order_cancellation(cancellation_id: str):
    try:
        result = await duffel.get(f"/air/order_cancellations/{cancellation_id}")
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)