import streamlit as st
import requests
import json

API_BASE = st.sidebar.text_input(
    "API Base URL", 
    value="http://localhost:8000/api",
    placeholder="http://localhost:8000/api"
)
st.title("Duffel API Management Console")

section = st.selectbox(
    "Select API Section",
    [
        "Offer Management",
        "Order Management",
        "Payments",
        "Post Booking",
        "Utils"
    ]
)

def safe_json_loads(txt):
    try:
        return json.loads(txt)
    except Exception as e:
        st.error(f"Invalid JSON: {e}")
        return None

def send_post(endpoint, payload):
    data = safe_json_loads(payload)
    if data is None:
        return
    resp = requests.post(f"{API_BASE}/{endpoint}", json=data)
    st.json(resp.json())

# ============ OFFER MANAGEMENT =============
if section == "Offer Management":
    st.header("Offer Management APIs")

    # Offer Requests
    st.subheader("Create Offer Request (POST)")
    offer_request_payload = st.text_area(
        "Offer Request Payload (JSON)", 
        value='''{
"slices": [{"origin": "JFK", "destination": "LHR", "departure_date": "2025-12-01"}],
"passengers": [{"type": "adult"}],
"cabin_class": "economy",
"supplier_timeout": 30,
"max_connections": 2
}''',
        placeholder='{\n"slices": [{"origin": "JFK", "destination": "LHR", "departure_date": "2025-12-01"}],\n"passengers": [{"type": "adult"}],\n"cabin_class": "economy",\n"supplier_timeout": 30,\n"max_connections": 2\n}'
    )
    if st.button("Create Offer Request"):
        send_post("offer-requests", offer_request_payload)

    st.subheader("List Offer Requests")
    offer_requests_limit = st.number_input(
        "Offer Requests Limit", min_value=1, value=10, 
        placeholder="10"
    )
    if st.button("List Offer Requests"):
        resp = requests.get(f"{API_BASE}/offer-requests", params={"limit": offer_requests_limit})
        st.json(resp.json())

    st.subheader("Get Offer Request by ID")
    offer_request_id = st.text_input(
        "Offer Request ID", 
        placeholder="e.g. offreq_abc123"
    )
    if st.button("Get Offer Request by ID"):
        resp = requests.get(f"{API_BASE}/offer-requests/{offer_request_id}")
        st.json(resp.json())

    # Offers
    st.subheader("List Offers for Offer Request")
    list_offers_offer_request_id = st.text_input(
        "Offer Request ID for Offers", 
        placeholder="e.g. offreq_abc123"
    )
    offers_limit = st.number_input(
        "Offers Limit", min_value=1, value=10, key="offers_limit",
        placeholder="10"
    )
    offers_sort = st.text_input(
        "Sort (optional)", "", key="offers_sort", 
        placeholder="price_total"
    )
    if st.button("List Offers"):
        params = {"offer_request_id": list_offers_offer_request_id, "limit": offers_limit}
        if offers_sort: params["sort"] = offers_sort
        resp = requests.get(f"{API_BASE}/offers", params=params)
        st.json(resp.json())

    st.subheader("Get Offer by ID")
    offer_id = st.text_input(
        "Offer ID", 
        placeholder="e.g. offer_abc123"
    )
    if st.button("Get Offer by ID"):
        resp = requests.get(f"{API_BASE}/offers/{offer_id}")
        st.json(resp.json())

    # Batch Offer Requests
    st.subheader("Create Batch Offer Request (POST)")
    batch_offer_payload = st.text_area(
        "Batch Offer Request Payload (JSON)", 
        value='''{
  // Place batch offer request payload here
}''',
        placeholder='{\n  // Place batch offer request payload here\n}'
    )
    if st.button("Create Batch Offer Request"):
        send_post("batch-offer-requests", batch_offer_payload)

    st.subheader("Get Batch Offer Request by ID")
    batch_offer_req_id = st.text_input(
        "Batch Offer Request ID", 
        placeholder="e.g. batchoffreq_abc123"
    )
    if st.button("Get Batch Offer Request"):
        resp = requests.get(f"{API_BASE}/batch-offer-requests/{batch_offer_req_id}")
        st.json(resp.json())

    # Partial Offer Requests
    st.subheader("Create Partial Offer Request (POST)")
    partial_offer_payload = st.text_area(
        "Partial Offer Request Payload (JSON)", 
        value='''{
  // Place partial offer request payload here
}''',
        placeholder='{\n  // Place partial offer request payload here\n}'
    )
    if st.button("Create Partial Offer Request"):
        send_post("partial-offer-requests", partial_offer_payload)

    st.subheader("Get Partial Offer Request by ID")
    partial_offer_req_id = st.text_input(
        "Partial Offer Request ID", 
        placeholder="e.g. poffreq_abc123"
    )
    selected_partial_offer_arr = st.text_area(
        "Selected Partial Offers (JSON array)", 
        value="[]",
        placeholder='["partial_offer_id_1", "partial_offer_id_2"]'
    )
    if st.button("Get Partial Offer Request"):
        arr = safe_json_loads(selected_partial_offer_arr)
        params = {"selected_partial_offer[]": arr} if arr else {}
        resp = requests.get(f"{API_BASE}/partial-offer-requests/{partial_offer_req_id}", params=params)
        st.json(resp.json())

    st.subheader("Get Full Offer Fares from Partial Offer Request")
    fares_partial_id = st.text_input(
        "Partial Offer Request ID for Fares", 
        placeholder="e.g. poffreq_abc123"
    )
    selected_partial_fares = st.text_area(
        "Selected Partial Offers for Fares (JSON array)", 
        value="[]",
        placeholder='["partial_offer_id_1", "partial_offer_id_2"]'
    )
    if st.button("Get Full Offer Fares"):
        arr = safe_json_loads(selected_partial_fares)
        params = {"selected_partial_offer[]": arr} if arr else {}
        resp = requests.get(f"{API_BASE}/partial-offer-requests/{fares_partial_id}/fares", params=params)
        st.json(resp.json())

# ============ ORDER MANAGEMENT =============
elif section == "Order Management":
    st.header("Order Management APIs")

    st.subheader("Create Order (POST)")
    order_payload = order_payload = st.text_area(
    "Order Payload (JSON)", 
    value='''{
    "type": "instant",
    "selected_offers": ["off_0000B1GWkOV9oEjCOw8epe"],
    "passengers": [
      {
        "id": "pas_0000B1GWkNxpo84ajaY2tO",
        "title": "mr",
        "given_name": "John",
        "family_name": "Doe",
        "gender": "m",
        "born_on": "1995-01-01",
        "email": "john.doe@example.com",
        "phone_number": "+441234567890"
      }
    ],
    "payments": [
      {
        "type": "balance",
        "amount": "287.99",
        "currency": "USD"
      }
    ],
        "metadata": {}
    }''',
        height=400,
        placeholder='{\n"type": "instant",\n"selected_offers": ["off_0000B1GWkOV9oEjCOw8epe"],\n"passengers": [{"id": "pas_0000B1GWkNxpo84ajaY2tO", "title": "mr", "given_name": "John", "family_name": "Doe", "gender": "m", "born_on": "1995-01-01", "email": "john.doe@example.com", "phone_number": "+441234567890"}],\n"payments": [{"type": "balance", "amount": "287.99", "currency": "USD"}],\n"metadata": {}\n}'
    )
    if st.button("Create Order"):
        send_post("orders", order_payload)

    st.subheader("List Orders")
    orders_limit = st.number_input(
        "Orders Limit", min_value=1, value=10, key="orders_limit",
        placeholder="10"
    )
    orders_sort = st.text_input(
        "Sort", "created_at", key="orders_sort", 
        placeholder="created_at"
    )
    if st.button("List Orders"):
        resp = requests.get(f"{API_BASE}/orders", params={"limit": orders_limit, "sort": orders_sort})
        st.json(resp.json())

    st.subheader("Get Order by ID")
    get_order_id = st.text_input(
        "Order ID", 
        placeholder="e.g. order_abc123"
    )
    if st.button("Get Order by ID"):
        resp = requests.get(f"{API_BASE}/orders/{get_order_id}")
        st.json(resp.json())

    # Airline Credits (related to orders)
    st.subheader("Create Airline Credit (POST)")
    airline_credit_payload = st.text_area(
        "Airline Credit Payload (JSON)", 
        value='''{
  // Place airline credit payload here
}''',
        placeholder='{\n  // Place airline credit payload here\n}'
    )
    if st.button("Create Airline Credit"):
        send_post("airline-credits", airline_credit_payload)

    st.subheader("List Airline Credits")
    user_id_credits = st.text_input(
        "User ID (optional for credits)", 
        placeholder="e.g. user_abc123"
    )
    credits_limit = st.number_input(
        "Airline Credits Limit", min_value=1, value=10, key="credits_limit",
        placeholder="10"
    )
    if st.button("List Airline Credits"):
        params = {"user_id": user_id_credits, "limit": credits_limit}
        resp = requests.get(f"{API_BASE}/airline-credits", params=params)
        st.json(resp.json())

    st.subheader("Get Airline Credit by ID")
    airline_credit_id = st.text_input(
        "Airline Credit ID", 
        placeholder="e.g. credit_abc123"
    )
    if st.button("Get Airline Credit by ID"):
        resp = requests.get(f"{API_BASE}/airline-credits/{airline_credit_id}")
        st.json(resp.json())

# ============ PAYMENTS =============
elif section == "Payments":
    st.header("Payments APIs")

    st.subheader("Create Payment (POST)")
    payment_payload = st.text_area(
        "Payment Payload (JSON)", 
        value='''{
"order_id": "your_order_id",
"payment": {"type": "credit_card", "amount": 10}
}''',
        placeholder='{\n"order_id": "your_order_id",\n"payment": {"type": "credit_card", "amount": 10}\n}'
    )
    if st.button("Create Payment"):
        send_post("payments", payment_payload)

    st.subheader("List Payments")
    payment_filter_order_id = st.text_input(
        "Order ID (optional, for filtering)", 
        placeholder="e.g. order_abc123"
    )
    payments_limit = st.number_input(
        "Payments Limit", min_value=1, value=10, key="payments_limit",
        placeholder="10"
    )
    if st.button("List Payments"):
        resp = requests.get(f"{API_BASE}/payments", params={"order_id": payment_filter_order_id, "limit": payments_limit})
        st.json(resp.json())

    st.subheader("Get Payment by ID")
    payment_id = st.text_input(
        "Payment ID", 
        placeholder="e.g. payment_abc123"
    )
    if st.button("Get Payment by ID"):
        resp = requests.get(f"{API_BASE}/payments/{payment_id}")
        st.json(resp.json())

# ============ POST BOOKING =============
elif section == "Post Booking":
    st.header("Post Booking APIs")

    # Order Cancellations (refunds etc.)
    st.subheader("Create Order Cancellation (POST)")
    cancellation_payload = st.text_area(
        "Order Cancellation Payload (JSON)",
        value='''{
"order_id": "your_order_id"
}''',
        placeholder='{\n"order_id": "your_order_id"\n}'
    )
    if st.button("Create Order Cancellation"):
        send_post("order-cancellations", cancellation_payload)

    st.subheader("List Order Cancellations")
    filter_order_id = st.text_input(
        "Order ID (optional, for filtering cancels)",
        placeholder="e.g. order_abc123"
    )
    cancellations_limit = st.number_input(
        "Order Cancellations Limit", min_value=1, value=10, key="cancellations_limit",
        placeholder="10"
    )
    if st.button("List Order Cancellations"):
        resp = requests.get(f"{API_BASE}/order-cancellations", params={"order_id": filter_order_id, "limit": cancellations_limit})
        st.json(resp.json())

    st.subheader("Get Order Cancellation by ID")
    cancellation_id = st.text_input(
        "Cancellation ID",
        placeholder="e.g. cancel_abc123"
    )
    if st.button("Get Order Cancellation by ID"):
        resp = requests.get(f"{API_BASE}/order-cancellations/{cancellation_id}")
        st.json(resp.json())

    # Order Changes
    st.subheader("Create Order Change Request (POST)")
    change_request_payload = st.text_area(
        "Order Change Request Payload (JSON)",
        value='''{
"order_id": "your_order_id",
"slices": {"add": [], "remove": []}
}''',
        placeholder='{\n"order_id": "your_order_id",\n"slices": {"add": [], "remove": []}\n}'
    )
    if st.button("Create Order Change Request"):
        send_post("order-changes/requests", change_request_payload)

    st.subheader("List Order Change Offers")
    change_offer_request_id = st.text_input(
        "Order Change Request ID",
        placeholder="e.g. ochangereq_abc123"
    )
    change_offer_sort = st.text_input(
        "Sort (optional for listing)",
        placeholder="price_total"
    )
    if st.button("List Order Change Offers"):
        params = {"order_change_request_id": change_offer_request_id}
        if change_offer_sort: params["sort"] = change_offer_sort
        resp = requests.get(f"{API_BASE}/order-changes/offers", params=params)
        st.json(resp.json())

    st.subheader("Get Order Change Offer by ID")
    order_change_offer_id = st.text_input(
        "Order Change Offer ID", 
        placeholder="e.g. ochangeoff_abc123"
    )
    if st.button("Get Order Change Offer by ID"):
        resp = requests.get(f"{API_BASE}/order-changes/offers/{order_change_offer_id}")
        st.json(resp.json())

    st.subheader("Create Pending Order Change (POST)")
    pending_order_change_payload = st.text_area(
        "Pending Order Change Payload (JSON)", 
        value='''{
"selected_order_change_offer": {}
}''',
        placeholder='{\n"selected_order_change_offer": {}\n}'
    )
    if st.button("Create Pending Order Change"):
        send_post("order-changes", pending_order_change_payload)

    st.subheader("Confirm Order Change (POST)")
    confirm_order_change_id = st.text_input(
        "Order Change ID",
        placeholder="e.g. ochange_abc123"
    )
    confirm_payment_payload = st.text_area(
        "Payment for Confirm (JSON)", 
        value='''{
"payment": {}
}''',
        placeholder='{\n"payment": {}\n}'
    )
    if st.button("Confirm Order Change"):
        send_post(f"order-changes/{confirm_order_change_id}/actions/confirm", confirm_payment_payload)

    # Airline-Initiated Changes (if supported in backend)
    # Add the UI and endpoint calls here if backend supports airline-initiated changes

# ============ UTILS =============
elif section == "Utils":
    st.header("Utils APIs")

    st.subheader("Check Health")
    if st.button("Check Health"):
        resp = requests.get(f"{API_BASE}/health")
        st.json(resp.json())

    st.subheader("Get Seat Maps by Offer ID")
    seat_map_offer_id = st.text_input(
        "Offer ID for Seat Map",
        placeholder="e.g. offer_abc123"
    )
    if st.button("Get Seat Maps"):
        resp = requests.get(f"{API_BASE}/seat-maps", params={"offer_id": seat_map_offer_id})
        st.json(resp.json())

# == Footer ==
st.markdown("---")
st.markdown("API Reference: [Duffel API v2 Documentation](https://duffel.com/docs/api/v2/)")
st.markdown("Built with Streamlit for rapid Duffel API management.") 