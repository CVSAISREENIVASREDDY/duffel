from fastapi import APIRouter, Depends, Query
from backend.models.duffel import CreateOrderBody
from backend.services.duffel_client import DuffelClient
from backend.utils.error_handlers import api_exception

router = APIRouter()
duffel = DuffelClient()

# backend/routers/orders.py

@router.post("/orders")
async def create_order(request: CreateOrderBody):
    try:
        payload = {"data": request.dict(exclude_none=True)}
        result = await duffel.post("/air/orders", payload)
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)

@router.get("/orders")
async def list_orders(limit: int = 50, sort: str = "created_at"):
    try:
        params = {"limit": limit, "sort": sort}
        result = await duffel.get("/air/orders", params)
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)

@router.get("/orders/{order_id}")
async def get_order(order_id: str):
    try:
        result = await duffel.get(f"/air/orders/{order_id}")
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)