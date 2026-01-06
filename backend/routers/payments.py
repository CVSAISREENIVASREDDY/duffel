from fastapi import APIRouter, Query
from services.duffel_client import DuffelClient
from utils.error_handlers import api_exception
from models.duffel import CreatePaymentRequest 

router = APIRouter()
duffel = DuffelClient()



@router.post("/payments")
async def create_payment(request: CreatePaymentRequest): # <--- Use the model here
    try:
        # We wrap the incoming JSON in "data" for the Duffel API
        payload = {"data": request.dict()}
        
        result = await duffel.post("/air/payments", payload)
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)

# ... keep list_payments and get_payment as they are ...

@router.get("/payments")
async def list_payments(order_id: str = None, limit: int = 50):
    try:
        params = {"order_id": order_id, "limit": limit}
        result = await duffel.get("/air/payments", params)
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e)

@router.get("/payments/{payment_id}")
async def get_payment(payment_id: str):
    try:
        result = await duffel.get(f"/air/payments/{payment_id}")
        return {"success": True, "data": result}
    except Exception as e:
        return api_exception(e) 