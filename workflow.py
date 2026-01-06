import streamlit as st
import requests
import json

# --- Configuration ---
API_BASE = st.sidebar.text_input("API Base URL", "http://localhost:8000/api")

st.title("Duffel Booking Workflow")

# --- Helper Functions ---
def get_offer_label(offer):
    if not isinstance(offer, dict):
        return str(offer)
    owner = offer.get('owner', {})
    airline_name = owner.get('name') or owner.get('iata_code') or "Unknown Airline"
    total = offer.get('total_amount', "N/A")
    currency = offer.get('total_currency', "N/A")
    oid = offer.get('id', "NoID")
    return f"{airline_name} | {total} {currency} | {oid}"

def safe_json_loads(txt):
    try:
        return json.loads(txt)
    except Exception as e:
        st.error(f"Invalid JSON: {e}")
        return None

# --- Session State Initialization ---
if "offer_request" not in st.session_state:
    st.session_state.offer_request = None
if "offers" not in st.session_state:
    st.session_state.offers = None
if "selected_offer" not in st.session_state:
    st.session_state.selected_offer = None
if "order" not in st.session_state:
    st.session_state.order = None
if "payment_response" not in st.session_state:
    st.session_state.payment_response = None

# View toggles
if "view_offer_req" not in st.session_state:
    st.session_state.view_offer_req = False
if "view_sel_offer" not in st.session_state:
    st.session_state.view_sel_offer = False
if "view_order_resp" not in st.session_state:
    st.session_state.view_order_resp = False
if "view_pay_resp" not in st.session_state:
    st.session_state.view_pay_resp = False

########## Step 1: Create Offer Request ##########
st.header("Step 1: Create Offer Request")
with st.form("offer_request_form"):
    slices = st.text_area(
        "Slices JSON",
        value='[{"origin":"JFK","destination":"LHR","departure_date":"2025-12-25"}]',
        placeholder='[{"origin":"JFK","destination":"LHR","departure_date":"2025-12-25"}]'
    )
    passengers = st.text_area(
        "Passengers JSON",
        value='[{"type": "adult"}]',
        placeholder='[{"type": "adult"}]'
    )
    cabin_class = st.selectbox(
        "Cabin Class",
        ["economy", "business", "first", "premium_economy"],
        index=0
    )
    supplier_timeout = st.number_input("Supplier Timeout (seconds)", min_value=1, value=30)
    max_connections = st.number_input("Max Connections", min_value=0, value=2)
    
    submitted = st.form_submit_button("1. Create Offer Request")
    
    if submitted:
        offer_req = {
            "slices": safe_json_loads(slices),
            "passengers": safe_json_loads(passengers),
            "cabin_class": cabin_class,
            "supplier_timeout": supplier_timeout,
            "max_connections": max_connections
        }
        with st.spinner("Searching for flights..."):
            resp = requests.post(f"{API_BASE}/offer-requests", json=offer_req)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("success"):
                    st.session_state.offer_request = data["data"]["data"]
                    # Reset downstream states
                    st.session_state.offers = None
                    st.session_state.selected_offer = None
                    st.session_state.order = None
                    st.session_state.payment_response = None
                else:
                    st.error("Failed to create offer request")
            else:
                st.error(f"API Error: {resp.status_code}")

if st.session_state.offer_request:
    if st.button("View Offer Request Response"):
        st.session_state.view_offer_req = not st.session_state.view_offer_req
    if st.session_state.view_offer_req:
        st.json(st.session_state.offer_request)

########## Step 2: Select Offer ##########
if st.session_state.offer_request:
    # --- SUCCESS BAR FOR STEP 1 ---
    st.success("✅ Step 1 Completed: Offer Request Created")
    
    st.header("Step 2: Select Offer")
    
    # Fetch offers if not already fetched
    if st.session_state.offers is None:
        offer_req_id = st.session_state.offer_request.get("id")
        with st.spinner("Fetching offers..."):
            resp = requests.get(f"{API_BASE}/offers", params={"offer_request_id": offer_req_id, "limit": 10})
            if resp.status_code == 200:
                data = resp.json()
                raw_offers = data.get("data", {}).get("offers", []) or data.get("data", {}).get("data", []) or []
                # Filter out non-dict entries if any
                st.session_state.offers = [o for o in raw_offers if isinstance(o, dict)]
            else:
                st.error("Failed to fetch offers.")

    offers = st.session_state.offers

    if offers:
        offer_options = {get_offer_label(offer): offer for offer in offers}
        selected_label = st.selectbox("Select an Offer", list(offer_options.keys()), key="select_offer")
        
        if st.button("2. Choose Offer"):
            st.session_state.selected_offer = offer_options[selected_label]
            st.session_state.view_sel_offer = False

        if st.session_state.selected_offer:
            if st.button("View Selected Offer Response"):
                st.session_state.view_sel_offer = not st.session_state.view_sel_offer
            if st.session_state.view_sel_offer:
                st.json(st.session_state.selected_offer)
    else:
        st.warning("No offers found.")

########## Step 3: Review and Create Order ##########
if st.session_state.selected_offer:
    # --- SUCCESS BARS FOR STEP 1 & 2 ---
    st.success("✅ Step 2 Completed: Offer Selected")

    st.header("Step 3: Review and Create Order")
    offer = st.session_state.selected_offer

    # --- 1. Offer & Payment Constraints ---
    total_amount = offer.get('total_amount', '0.00')
    total_currency = offer.get('total_currency', 'USD')
    
    # Check if airline forces instant payment
    payment_reqs = offer.get("payment_requirements", {})
    requires_instant = payment_reqs.get("requires_instant_payment", False)
    payment_deadline = payment_reqs.get("payment_required_by")

    st.subheader(f"Total: {total_amount} {total_currency}")
    
    # --- 2. Select Order Type ---
    # Logic: If instant is required, force it. Otherwise, let user choose.
    if requires_instant:
        st.warning("⚠️ This offer requires immediate payment.")
        order_type_choice = "Pay Now (Instant)"
        st.radio("Order Type", ["Pay Now (Instant)"], disabled=True)
    else:
        st.success(f"✅ You can hold this price until {payment_deadline}")
        order_type_choice = st.radio(
            "How would you like to proceed?",
            ["Hold (Pay Later)", "Pay Now (Instant)"],
            index=0
        )

    # Map label to API value
    is_instant = (order_type_choice == "Pay Now (Instant)")
    api_order_type = "instant" if is_instant else "hold"

    # --- 3. Payment Details (Conditional) ---
    payment_payload_list = []
    
    if is_instant:
        st.markdown("### 💳 Payment Details")
        col1, col2 = st.columns(2)
        with col1:
            # "balance" is the standard test method in Duffel Sandbox
            pay_method = st.selectbox("Payment Method", ["balance", "arc_bsp_cash"], key="pay_method_step3")
        with col2:
            pay_amt = st.text_input("Amount", value=total_amount, disabled=True, key="pay_amt_step3")
            
        payment_payload_list = [{
            "type": pay_method,
            "amount": pay_amt,
            "currency": total_currency
        }]
    else:
        st.info("ℹ️ No payment required now. You will receive a booking reference immediately.")

    # --- 4. Passenger Details (User Input with Defaults) ---
    origin_passengers = offer.get("passengers", [])
    enriched_passengers = []
    
    st.subheader("Passenger Details")
    st.info("Passenger details are pre-filled. You can edit them if needed.")

    # Loop through passengers from the offer to generate input fields
    for idx, p in enumerate(origin_passengers):
        st.markdown(f"**Passenger {idx + 1} ({p.get('type', 'adult')})**")
        
        # Row 1: Name (Defaults set to your original data)
        c1, c2, c3 = st.columns([1, 2, 2])
        with c1:
            title = st.selectbox("Title", ["mr", "ms", "mrs", "miss"], index=1, key=f"title_{idx}") # Default: ms
        with c2:
            given_name = st.text_input("Given Name", value="Amelia", key=f"given_name_{idx}")
        with c3:
            family_name = st.text_input("Family Name", value="Earhart", key=f"family_name_{idx}")
        
        # Row 2: Details
        c4, c5, c6 = st.columns(3)
        with c4:
            born_on = st.text_input("Date of Birth", value="1987-07-24", key=f"dob_{idx}")
        with c5:
            gender = st.selectbox("Gender", ["m", "f"], index=1, key=f"gender_{idx}") # Default: f
        with c6:
            email = st.text_input("Email", value="amelia.earhart@example.com", key=f"email_{idx}")
            
        # Row 3: Phone
        phone_number = st.text_input("Phone Number", value="+442080160509", key=f"phone_{idx}")
        
        st.markdown("---")

        # Build the passenger object
        enriched_p = {
            "id": p.get("id"),
            "type": p.get("type", "adult"),
            "given_name": given_name,
            "family_name": family_name,
            "born_on": born_on,
            "title": title,
            "gender": gender,
            "email": email,
            "phone_number": phone_number
        }
        enriched_passengers.append(enriched_p)

    # --- 5. Submit Order ---
    btn_label = "Confirm & Pay" if is_instant else "Confirm Hold Order"
    if st.button(f"3. {btn_label}"):
        
        # Validation: Check if names are empty
        missing_fields = any(not p['given_name'] or not p['family_name'] for p in enriched_passengers)
        
        if missing_fields:
            st.error("⚠️ Please fill in at least the Given Name and Family Name for all passengers.")
        else:
            # Build Payload
            order_body = {
                "type": api_order_type,
                "selected_offers": [offer.get("id")],
                "passengers": enriched_passengers,
                "metadata": {"source": "streamlit_demo_v2"}
            }

            # CRITICAL: Only add 'payments' key if it is Instant
            if is_instant:
                order_body["payments"] = payment_payload_list
            
            with st.spinner(f"Creating {api_order_type} order..."):
                resp = requests.post(f"{API_BASE}/orders", json=order_body)
                
                # Handle Response
                if resp.status_code in [200, 201]:
                    data = resp.json()
                    if data.get("success"):
                        order_data = data["data"]["data"]
                        st.session_state.order = order_data
                        
                        ref = order_data.get('booking_reference')
                        st.success(f"🎉 Order Created! Reference: **{ref}**")
                        
                        if not is_instant:
                            st.info("Go to Step 4 to complete payment for this hold.")
                        else:
                            st.session_state.payment_response = {"status": "Already Paid"}
                            
                        st.session_state.view_order_resp = False
                    else:
                        st.error("Duffel API returned failure.")
                        st.json(data)
                else:
                    st.error(f"Request Failed: {resp.status_code}")
                    try:
                        st.json(resp.json())
                    except:
                        st.write(resp.text)

    # View Response Toggle
    if st.session_state.order:
        if st.button("View Order Response"):
            st.session_state.view_order_resp = not st.session_state.view_order_resp
        if st.session_state.view_order_resp:
            st.json(st.session_state.order)

########## Step 4: Make Payment ##########
if st.session_state.order:
 
    st.header("Step 4: Make Payment")
    
    # 1. Get Order Details
    order = st.session_state.order
    order_id = order.get("id")
    payment_status = order.get("payment_status", {})
    
    # Check if 'awaiting_payment' is None (instant order) or False (paid)
    is_paid = payment_status.get("awaiting_payment") is False
    
    # 2. Check if already paid
    if is_paid:
        st.success("✅ This order is paid ")
        if order.get('booking_reference'):
            st.write(f"**Booking Reference:** {order.get('booking_reference')}")
    else:
        # 3. Display Payment Due
        total_price = order.get("total_amount", "0.00")
        currency = order.get("total_currency", "USD")
        deadline = payment_status.get("payment_required_by", "Unknown")

        st.warning(f"⚠️ Payment of **{total_price} {currency}** is required by {deadline}")
        st.write(f"**Order ID:** `{order_id}`")

        # 4. Payment Input Form
        with st.form("payment_form"):
            col1, col2 = st.columns(2)
            with col1:
                payment_type = st.selectbox("Payment Type", ["balance", "arc_bsp_cash"])
            with col2:
                payment_amount = st.text_input("Amount", value=total_price, disabled=True)
            
            pay_clicked = st.form_submit_button("4. Pay Now & Issue Ticket")

        if pay_clicked:
            payment_body = {
                "order_id": order_id,
                "payment": {
                    "type": payment_type,
                    "amount": payment_amount,
                    "currency": currency
                }
            }
            
            with st.spinner("Processing Payment & Issuing Ticket..."):
                resp = requests.post(f"{API_BASE}/payments", json=payment_body)
                
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("success"):
                        st.session_state.payment_response = data["data"]
                        
                        # --- FIX: REFRESH ORDER LOGIC ---
                        # Fetch the updated order to get the new 'documents' and 'payment_status'
                        refresh_resp = requests.get(f"{API_BASE}/orders/{order_id}")
                        if refresh_resp.status_code == 200:
                            updated_order = refresh_resp.json()["data"]["data"]
                            st.session_state.order = updated_order
                        else:
                            st.warning("Payment successful, but failed to refresh order details.")

                        st.balloons()
                        st.success("🎉 Payment Successful! Redirecting...")
                        st.session_state.view_pay_resp = False
                        
                        # Force Rerun to immediately show Step 5
                        st.rerun()
                    else:
                        st.error("Payment Failed")
                        st.json(data)
                else:
                    st.error(f"API Error: {resp.status_code}")
                    try:
                        st.json(resp.json())
                    except:
                        st.write(resp.text)

    # 5. View Payment Response Toggle
    if st.session_state.payment_response:
        if st.button("View Payment Response"):
            st.session_state.view_pay_resp = not st.session_state.view_pay_resp
        if st.session_state.view_pay_resp:
            st.json(st.session_state.payment_response)

########## Step 5: Booking Confirmation & Documents ##########
# Show this step if we have an order and it is NOT awaiting payment (i.e., it is Paid)
if st.session_state.order and st.session_state.order.get("payment_status", {}).get("awaiting_payment") is False:
    st.header("Step 5: Booking Confirmation & E-Tickets")
    
    order_id = st.session_state.order.get("id")
    final_order = st.session_state.order
    
    # Display Order Summary
    st.markdown(f"### 🎫 Booking Reference: `{final_order.get('booking_reference')}`")
    st.success("Your booking is confirmed and ticketed.")

    # Display Documents (E-Tickets)
    documents = final_order.get("documents", [])
    
    if documents:
        st.write("### 📂 Travel Documents")
        for doc in documents:
            doc_type = doc.get("type", "Unknown Type").replace("_", " ").title()
            unique_id = doc.get("unique_identifier", "N/A")
            
            with st.container():
                st.info(f"**{doc_type}**: `{unique_id}`")
    else:
        st.warning("No documents found yet. The airline might still be issuing them.")
        if st.button("🔄 Refresh Documents"):
            with st.spinner("Fetching official documents..."):
                resp = requests.get(f"{API_BASE}/orders/{order_id}")
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state.order = data["data"]["data"]
                    st.rerun()
                else:
                    st.error("Failed to refresh order details.")

    # Debug View
    with st.expander("View response"):
        st.json(final_order)

st.markdown("---")
st.markdown("End-to-end Duffel workflow demo. [Duffel Docs](https://duffel.com/docs/api/v2/)") 