from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class AirlineCredit(BaseModel):
    airline_iata_code: str
    amount: str
    amount_currency: str
    code: str
    issued_on: Optional[str]
    expires_on: Optional[str]
    passenger_id: Optional[str]

class OfferCreateRequest(BaseModel):
    slices: List[Dict]
    passengers: List[Dict]
    cabin_class: str = Field(..., pattern="^(economy|business|first|premium_economy)$")
    return_offers: bool = True
    supplier_timeout: Optional[int]
    max_connections: Optional[int]

class CreateOrderBody(BaseModel):
    type: str = Field(..., pattern="^(instant|hold)$")
    selected_offers: List[str]
    passengers: List[Dict]
    payments: Optional[List[Dict]] = None  
    metadata: Optional[Dict[str, str]]

class CreatePaymentRequest(BaseModel):
    order_id: str
    payment: Dict 
# Add more as needed, following your Duffel business logic and API contract 