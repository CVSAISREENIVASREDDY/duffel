from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import (
    offers, offer_requests, orders, payments, seat_maps,
    order_cancellations, order_changes, partial_offer_requests,
    batch_offer_requests, airline_credits
)

from backend.utils.error_handlers import api_exception

app = FastAPI(
    title="Duffel Python API",
    description="Best-practice FastAPI backend for Duffel APIs.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    print(f"{request.method} {request.url.path}")
    return await call_next(request)

@app.get("/")
def root():
    return {
        "message": "Duffel Python API",
        "endpoints": [
            "/api/health",
            "/api/offers",
            "/api/offer-requests",
            "/api/orders",
            "/api/payments",
            "/api/seat-maps",
            "/api/order-cancellations",
            "/api/order-changes",
            "/api/partial-offer-requests",
            "/api/batch-offer-requests",
            "/api/airline-credits"
        ]
    }

@app.get("/api/health")
def health():
    from datetime import datetime
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return api_exception(exc)

# Register all routers
app.include_router(offers.router, prefix="/api")
app.include_router(offer_requests.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(payments.router, prefix="/api")
app.include_router(seat_maps.router, prefix="/api")
app.include_router(order_cancellations.router, prefix="/api")
app.include_router(order_changes.router, prefix="/api")
app.include_router(partial_offer_requests.router, prefix="/api")
app.include_router(batch_offer_requests.router, prefix="/api")
app.include_router(airline_credits.router, prefix="/api") 