# ------------------------------------------------------------
# cafe.py  –  Café Management System (coffee-brown theme)
# ------------------------------------------------------------
import json, os, io
from datetime import datetime, date
import streamlit as st
import qrcode
from bill_mail import build_pdf, send_email

# ---------- GLOBAL COFFEE-THEME ----------
st.set_page_config(page_title="Café Management System", page_icon="☕", layout="wide")

st.markdown(
    """
    <style>
    /* Page background & default text */
    .main {background-color: #fdf6f0; color: #3e2723;}

    /* Sidebar */
    .css-1d391kg {background-color: #efebe9 !important;}

    /* All Buttons */
    .stButton > button {
        background-color: #8d6e63;
        color: #ffffff;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        transition: background-color 0.2s;
    }
    .stButton > button:hover {background-color: #6d4c41;}

    /* All Select Boxes, Number Inputs, Text Inputs, Multiselect, Date Inputs */
    .stSelectbox > div > div > div,
    .stMultiSelect > div > div > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #fff8e1;
        border: 1px solid #a1887f;
        border-radius: 6px;
        color: #3e2723;
    }

    /* Checkbox color */
    .stCheckbox > div > div > div {
        accent-color: #8d6e63;
    }

    /* Radio color */
    .stRadio > div > div > div {
        accent-color: #8d6e63;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: #efebe9;
        border-left: 5px solid #8d6e63;
        padding: 0.5rem;
    }

    /* Sidebar headings */
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #5d4037;
    }

    /* Expander headers */
    .streamlit-expanderHeader {
        background-color: #efebe9;
        color: #5d4037;
        border-radius: 6px;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #efebe9;
        color: #5d4037;
        border-radius: 6px 6px 0 0;
        border-bottom: 2px solid #8d6e63;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #8d6e63;
        color: #ffffff;
    }

    /* Login hero background */
    .login-hero {
        background-image: url("https://images.unsplash.com/photo-1511920170033-f8396924c3cb?auto=format&fit=crop&w=1350&q=80");
        background-size: cover;
        background-position: center;
        padding: 100px 0;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# ---------- Café-Brown Global Skin ----------
st.markdown(
    """
    <style>
    /* Page background */
    .stApp {
        background: linear-gradient(135deg, #fdf6f0 0%, #efebe9 100%);
    }

    /* Header / Sidebar titles */
    h1, h2, h3, h4, .stSidebar h1, .stSidebar h2 {
        color: #5d4037 !important;
    }

    /* Buttons everywhere */
    .stButton > button {
        background: linear-gradient(135deg, #8d6e63, #6d4c41);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.5em 1.2em;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #6d4c41, #5d4037);
        transform: translateY(-1px);
    }

    /* Inputs, Select Boxes, Date Picker, Text Area, Checkboxes, Radio */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div,
    .stMultiSelect > div > div > div,
    .stDateInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stCheckbox input,
    .stRadio input {
        background-color: #fff8e1 !important;
        border: 1px solid #a1887f !important;
        border-radius: 6px;
        color: #3e2723;
    }

    /* Sidebar */
    .css-1d391kg {
        background: #efebe9 !important;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: #fff8e1;
        border-left: 5px solid #8d6e63;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {
        background: #efebe9;
        color: #5d4037;
        border-radius: 6px 6px 0 0;
        margin-right: 4px;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: #8d6e63;
        color: #ffffff;
    }

    /* Expanders / Accordions */
    .streamlit-expanderHeader {
        background-color: #efebe9;
        color: #5d4037;
        border-radius: 6px;
        border-left: 4px solid #8d6e63;
    }

    /* Tables & Dataframes */
    .dataframe th {
        background-color: #8d6e63 !important;
        color: #ffffff;
    }
    .dataframe td {
        background-color: #fff8e1;
        color: #3e2723;
    }

    /* Login hero background */
    .login-hero {
    background-image: url("https://images.unsplash.com/photo-1511920170033-f8396924c3cb?auto=format&fit=crop&w=1350&q=80");
}
        background-size: cover;
        background-position: center;
        padding: 100px 0;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# 🔥 Force-style ALL remaining buttons
st.markdown(
    """
    <style>
    /* Settings-page buttons */
    .stFormSubmitButton > button,
    .stButton > button,
    /* Item-card buttons (Update / Delete) */
    div[data-testid="stFormSubmitButton"] button,
    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #8d6e63, #6d4c41) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.4em 1em !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
        transition: all 0.2s !important;
    }
    .stFormSubmitButton > button:hover,
    .stButton > button:hover {
        background: linear-gradient(135deg, #6d4c41, #5d4037) !important;
        transform: translateY(-1px) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <style>
    /* Settings page number-input fields */
    .stNumberInput > div > div > input {
        background-color: #fff8e1 !important;
        border: 1px solid #8d6e63 !important;
        border-radius: 6px !important;
        color: #3e2723 !important;
        padding: 0.3em 0.5em !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <style>
    /* Make category titles bold & bigger */
    .stTabs > div > div > div > div > div > div {
        font-weight: 800 !important;
        font-size: 1.1em !important;
        color: #5d4037 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    /* 🎯 Tax-Rate & Service-Charge fields */
    input[type="number"] {
        background-color: #fff8e1 !important;
        border: 1px solid #8d6e63 !important;
        border-radius: 6px !important;
        color: #3e2723 !important;
        padding: 0.35em 0.5em !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <style>
    /* 🔽 Shrink the "Filter by Status" dropdown text */
    div[data-baseweb="select"] span {
        font-size: 0.70em !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)




# ---------- File paths ----------
MENU_FILE = "menu_data.json"
ORDERS_FILE = "orders_data.json"
SETTINGS_FILE = "settings.json"
TABLES_FILE = "tables_data.json"
USERS_FILE = "users_data.json"

# ---------- Load / Save helpers ----------
def load_json(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception:
        return None

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

# ---------- Initialize ----------
def initialize_data_files():
    if not os.path.exists(MENU_FILE):
        default_menu = {
            "beverages": [
                {"id": "BEV001", "name": "Espresso", "price": 2.50, "category": "Coffee",
                 "available": True, "description": "Strong black coffee", "inventory": 50},
                {"id": "BEV002", "name": "Cappuccino", "price": 3.50, "category": "Coffee",
                 "available": True, "description": "Coffee with steamed milk foam", "inventory": 40},
                {"id": "BEV003", "name": "Latte", "price": 4.00, "category": "Coffee",
                 "available": True, "description": "Coffee with steamed milk", "inventory": 40},
                {"id": "BEV004", "name": "Green Tea", "price": 2.00, "category": "Tea",
                 "available": True, "description": "Fresh green tea", "inventory": 30},
                {"id": "BEV005", "name": "Fresh Orange Juice", "price": 3.00, "category": "Juice",
                 "available": True, "description": "Freshly squeezed orange juice", "inventory": 25}
            ],
            "food": [
                {"id": "FOOD001", "name": "Croissant", "price": 2.50, "category": "Pastry",
                 "available": True, "description": "Buttery French pastry", "inventory": 40},
                {"id": "FOOD002", "name": "Chocolate Muffin", "price": 3.00, "category": "Pastry",
                 "available": True, "description": "Rich chocolate muffin", "inventory": 35},
                {"id": "FOOD003", "name": "Caesar Salad", "price": 8.50, "category": "Salad",
                 "available": True, "description": "Fresh romaine with caesar dressing", "inventory": 20},
                {"id": "FOOD004", "name": "Club Sandwich", "price": 9.00, "category": "Sandwich",
                 "available": True, "description": "Triple layer sandwich with turkey and bacon", "inventory": 30},
                {"id": "FOOD005", "name": "Margherita Pizza", "price": 12.00, "category": "Pizza",
                 "available": True, "description": "Classic pizza with tomato and mozzarella", "inventory": 15}
            ]
        }
        save_json(MENU_FILE, default_menu)

    for f, default in [
        (ORDERS_FILE, []),
        (SETTINGS_FILE, {"cafe_name": "My Café", "barcode_url": "https://mycafe.com/menu", "tax_rate": 0.10, "service_charge": 0.05}),
        (TABLES_FILE, [{"table_number": str(i), "status": "Available"} for i in range(1, 11)]),
        (USERS_FILE, [{"username": "admin", "password": "admin123", "role": "admin"},
                      {"username": "staff", "password": "staff123", "role": "staff"}])
    ]:
        if not os.path.exists(f):
            save_json(f, default)

initialize_data_files()

# ---------- Auth ----------
def authenticate(username, password):
    users = load_json(USERS_FILE) or []
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user
    return None

# ---------- Login ----------
def login_page():
    st.markdown('<div class="login-hero"><h1>☕ Café Management System</h1></div>', unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = authenticate(username, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["user"] = user
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---------- Pages (unchanged logic) ----------
def dashboard_page():
    st.header("🏠 Dashboard")
    menu_data = load_json(MENU_FILE) or {"beverages": [], "food": []}
    orders_data = load_json(ORDERS_FILE) or []
    total_items = sum(len(menu_data[k]) for k in menu_data)
    total_orders = len(orders_data)
    today_orders = [o for o in orders_data if o.get("date") == str(date.today())]
    today_revenue = sum(o["total"] for o in today_orders)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Menu Items", total_items)
    col2.metric("Total Orders", total_orders)
    col3.metric("Today's Orders", len(today_orders))
    col4.metric("Today's Revenue", f"₹{today_revenue:.2f}")

def menu_management_page():
    st.header("📋 Menu Management")
    menu_data = load_json(MENU_FILE) or {"beverages": [], "food": []}
    tab1, tab2, tab3 = st.tabs(["View Menu", "Add Item", "Edit Items"])
    # (your existing inner code unchanged)
    with tab1:
        st.subheader("Current Menu")
        for category in ["beverages", "food"]:
            st.write(f"### {category.capitalize()}")
            items = menu_data.get(category, [])
            if not items:
                st.info("No items in this category.")
            else:
                for item in items:
                    st.write(
                        f"{item['name']} — ₹{item['price']:.2f} — Inv: {item.get('inventory', 'N/A')} — {'✅' if item['available'] else '❌'}")
                    if item.get('description'):
                        st.write(f"{item['description']}")
    with tab2:
        st.subheader("Add New Item")
        with st.form("add_item_form"):
            item_type = st.selectbox("Item Type", ["beverages", "food"])
            item_name = st.text_input("Item Name")
            item_price = st.number_input("Price (₹)", min_value=0.01, step=0.01)
            item_category = st.text_input("Category")
            item_description = st.text_area("Description")
            item_inventory = st.number_input("Inventory Quantity", min_value=0, step=1)
            item_available = st.checkbox("Available", value=True)
            submitted = st.form_submit_button("Add Item")
            if submitted:
                if item_name and item_price and item_category:
                    prefix = "BEV" if item_type == "beverages" else "FOOD"
                    existing = menu_data.get(item_type, [])
                    max_id = 0
                    for itm in existing:
                        try:
                            num = int(itm["id"].replace(prefix, ""))
                            if num > max_id:
                                max_id = num
                        except:
                            continue
                    new_id = f"{prefix}{max_id + 1:03d}"
                    new_item = {
                        "id": new_id, "name": item_name, "price": float(item_price),
                        "category": item_category, "available": item_available,
                        "description": item_description, "inventory": int(item_inventory)
                    }
                    if item_type not in menu_data:
                        menu_data[item_type] = []
                    menu_data[item_type].append(new_item)
                    save_json(MENU_FILE, menu_data)
                    st.success(f"Added {item_name} to menu!")
                else:
                    st.error("Please fill all fields.")
    with tab3:
        st.subheader("Edit Menu Items")
        all_items = []
        for t, items in menu_data.items():
            for itm in items:
                itm["_type"] = t
                all_items.append(itm)
        if not all_items:
            st.info("No items to edit.")
            return
        options = [f"{i['name']} ({i['_type']})" for i in all_items]
        choice = st.selectbox("Select item", options)
        idx = options.index(choice)
        item = all_items[idx]
        with st.form("edit_item_form"):
            new_name = st.text_input("Name", value=item["name"])
            new_price = st.number_input("Price (₹)", min_value=0.01, value=item["price"])
            new_category = st.text_input("Category", value=item["category"])
            new_description = st.text_area("Description", value=item.get("description", ""))
            new_inventory = st.number_input("Inventory Quantity", min_value=0, value=item.get("inventory", 0))
            new_available = st.checkbox("Available", value=item["available"])
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Update Item"):
                    t = item["_type"]
                    for i, itm in enumerate(menu_data[t]):
                        if itm["id"] == item["id"]:
                            menu_data[t][i].update({
                                "name": new_name, "price": float(new_price),
                                "category": new_category, "description": new_description,
                                "inventory": int(new_inventory), "available": new_available
                            })
                            save_json(MENU_FILE, menu_data)
                            st.success("Item updated.")
                            st.rerun()
            with col2:
                if st.form_submit_button("Delete Item"):
                    t = item["_type"]
                    menu_data[t] = [itm for itm in menu_data[t] if itm["id"] != item["id"]]
                    save_json(MENU_FILE, menu_data)
                    st.success("Item deleted.")
                    st.rerun()

def table_management_page():
    st.header("🪑 Live Table Status")

    def is_table_busy(tn: str) -> bool:
        orders = load_json(ORDERS_FILE) or []
        return any(
            o.get("table_number") == tn
            and o.get("status") in {"Pending", "Preparing", "Ready"}
            for o in orders
        )

    # refresh status
    tables = [{"table_number": str(i),
               "status": "Busy" if is_table_busy(str(i)) else "Available"}
              for i in range(1, 11)]
    save_json(TABLES_FILE, tables)

    # display
    for t in tables:
        col1, col2 = st.columns(2)
        col1.write(t["table_number"])
        col2.write(t["status"])
    # --- auto-update statuses -------------------------------------
    changed = False
    for t in tables:
        should_be = "Occupied" if is_table_busy(t["table_number"]) else "Available"
        if t["status"] != should_be:
            t["status"] = should_be
            changed = True
    if changed:
        save_json(TABLES_FILE, tables)

    # --- display & allow manual override --------------------------
    status_options = ["Available", "Occupied", "Reserved"]
    manual_change = False
    for idx, table in enumerate(tables):
        col1, col2, col3 = st.columns([1, 2, 1])
        col1.write(table["table_number"])
        col2.write(table["status"])
        new_status = col3.selectbox(
            "Change",
            status_options,
            index=status_options.index(table["status"]),
            key=f"tbl_{table['table_number']}"
        )
        if new_status != table["status"]:
            tables[idx]["status"] = new_status
            manual_change = True
    if manual_change:
        save_json(TABLES_FILE, tables)
        st.success("Table statuses updated")



def order_management_page():
    st.header("🛒 Order Management")
    menu_data = load_json(MENU_FILE) or {"beverages": [], "food": []}
    orders_data = load_json(ORDERS_FILE) or []
    settings = load_json(SETTINGS_FILE) or {}
    tab1, tab2 = st.tabs(["New Order", "Order History"])
    with tab1:
        st.subheader("Create New Order")
        col_left, col_mid, col_right = st.columns(3)
        with col_left:
            customer_name = st.text_input("Customer Name")
        with col_right:
            customer_email = st.text_input("Customer e-mail (for bill)")
        busy = {o.get("table_number") for o in orders_data
                if o.get("table_number") and o.get("status") in {"Pending", "Preparing", "Ready"}}
        free = [str(i) for i in range(1, 11) if str(i) not in busy]
        if free:
            table_number = col_mid.selectbox("Table Number", ["No table"] + free)
        else:
            st.warning("⚠ All tables are occupied.")
            table_number = "No table"
        st.write("### Menu Items")
        all_items = [it for cat in menu_data.values() for it in cat if it.get("available", True)]
        for cat in sorted({it["category"] for it in all_items}):
            st.write(f"{cat}")
            for item in [i for i in all_items if i["category"] == cat]:
                c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                c1.write(f"{item['name']} — {item.get('description', '')}")
                c2.write(f"₹{item['price']:.2f}")
                qty = c3.number_input(f"Qty {item['id']}", 0, 100, key=f"qty_{item['id']}")
                if c4.button("Add", key=f"add_{item['id']}") and qty > 0:
                    if qty > item.get("inventory", 0):
                        st.error(f"Only {item['inventory']} left of {item['name']}")
                    else:
                        st.session_state.cart.append({
                            "id": item["id"], "name": item["name"],
                            "price": item["price"], "quantity": qty,
                            "subtotal": round(item["price"] * qty, 2)
                        })
                        st.success(f"Added {qty}x {item['name']} to cart!")
                        st.rerun()

        st.subheader("Shopping Cart")
        if st.session_state.cart:
            total = sum(i["subtotal"] for i in st.session_state.cart)
            tax_rate = settings.get("tax_rate", 0.10)
            service_charge = settings.get("service_charge", 0.05)
            tax_amt = total * tax_rate
            svc_amt = total * service_charge
            final_total = total + tax_amt + svc_amt
            st.write(f"Subtotal: ₹{total:.2f}")
            st.write(f"Tax: ₹{tax_amt:.2f}")
            st.write(f"Service Charge: ₹{svc_amt:.2f}")
            st.write(f"Total: ₹{final_total:.2f}")
            payment_status = st.selectbox("Payment Status", ["Unpaid", "Paid", "Partial"])
            if st.button("Place Order"):
                if not customer_name:
                    st.error("Enter customer name")
                elif not st.session_state.cart:
                    st.error("Cart is empty")
                else:
                    for ci in st.session_state.cart:
                        for cat in menu_data:
                            for it in menu_data[cat]:
                                if it["id"] == ci["id"]:
                                    if ci["quantity"] > it.get("inventory", 0):
                                        st.error(f"Not enough inventory for {it['name']}")
                                        return
                                    it["inventory"] -= ci["quantity"]
                    save_json(MENU_FILE, menu_data)
                    new_order = {
                        "id": f"ORD{len(orders_data) + 1:05d}",
                        "customer_name": customer_name,
                        "table_number": table_number if table_number != "No table" else "",
                        "items": st.session_state.cart.copy(),
                        "subtotal": total,
                        "tax": tax_amt,
                        "service_charge": svc_amt,
                        "total": final_total,
                        "date": str(date.today()),
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "timestamp": datetime.now().isoformat(),
                        "status": "Pending",
                        "payment_status": payment_status
                    }
                    orders_data.append(new_order)
                    save_json(ORDERS_FILE, orders_data)
                    try:
                        pdf_bytes = build_pdf(new_order)
                    except Exception as e:
                        st.error(f"Error generating PDF: {e}")
                        pdf_bytes = None
                    if customer_email and pdf_bytes:
                        try:
                            send_email(customer_email, new_order, pdf_bytes)
                            st.success(f"Bill sent to {customer_email}")
                        except Exception as e:
                            st.error(f"Email send failed: {e}")
                    if pdf_bytes:
                        st.download_button("📄 Download Bill PDF", pdf_bytes,
                                           file_name=f"{new_order['id']}.pdf", mime="application/pdf")
                    st.success(f"Order placed! ID: {new_order['id']}")
                    st.session_state.cart = []
        else:
            st.info("Add items to the cart from above menu.")

    with tab2:
        st.subheader("Order History")
        orders = load_json(ORDERS_FILE) or []
        if not orders:
            st.info("No orders found")
            return
        status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Preparing", "Ready", "Completed", "Cancelled"])
        date_filter = st.date_input("Filter by Date", None)
        filt = orders
        if status_filter != "All":
            filt = [o for o in filt if o.get("status") == status_filter]
        if date_filter:
            filt = [o for o in filt if o.get("date") == str(date_filter)]
        filt = sorted(filt, key=lambda x: x["timestamp"], reverse=True)
        for order in filt:
            with st.expander(f"{order['id']} by {order['customer_name']} — ₹{order['total']:.2f} ({order.get('status')})"):
                st.write(f"Date: {order['date']} {order['time']} | Table: {order.get('table_number', '-')}")
                for it in order["items"]:
                    st.write(f"- {it['name']} x{it['quantity']} = ₹{it['subtotal']:.2f}")
                st.write(f"Subtotal: ₹{order['subtotal']:.2f}")
                st.write(f"Tax: ₹{order.get('tax', 0):.2f}")
                st.write(f"Service Charge: ₹{order.get('service_charge', 0):.2f}")
                st.write(f"Total: ₹{order['total']:.2f}")
                st.write(f"Payment: {order.get('payment_status', 'Unpaid')}")
                new_status = st.selectbox("Update Status", ["Pending", "Preparing", "Ready", "Completed", "Cancelled"],
                                          index=["Pending", "Preparing", "Ready", "Completed", "Cancelled"].index(
                                              order.get("status", "Pending")),
                                          key=f"status_{order['id']}")
                if st.button("Update", key=f"upd_{order['id']}"):
                    for o in orders:
                        if o["id"] == order["id"]:
                            o["status"] = new_status
                            save_json(ORDERS_FILE, orders)
                            st.success("Status updated")
                            st.rerun()

def sales_analytics_page():
    st.header("📊 Sales Analytics")
    orders_data = load_json(ORDERS_FILE) or []
    if not orders_data:
        st.info("No sales data available.")
        return
    start_date = st.date_input("Start Date", value=date.today().replace(day=1))
    end_date = st.date_input("End Date", value=date.today())
    filtered = [o for o in orders_data if start_date <= datetime.strptime(o['date'], "%Y-%m-%d").date() <= end_date]
    if not filtered:
        st.warning("No orders in selected date range")
        return
    total_revenue = sum(o['total'] for o in filtered)
    total_orders = len(filtered)
    avg_order = total_revenue / total_orders if total_orders else 0
    st.metric("Total Revenue", f"₹{total_revenue:.2f}")
    st.metric("Total Orders", total_orders)
    st.metric("Average Order Value", f"₹{avg_order:.2f}")
    st.subheader("Daily Revenue")
    daily_sales = {}
    for o in filtered:
        daily_sales[o['date']] = daily_sales.get(o['date'], 0) + o['total']
    for d, rev in sorted(daily_sales.items()):
        st.write(f"{d}: ₹{rev:.2f}")
    st.subheader("Top Selling Items")
    item_sales = {}
    for o in filtered:
        for item in o['items']:
            name = item['name']
            item_sales.setdefault(name, 0)
            item_sales[name] += item['quantity']
    for item_name, qty in sorted(item_sales.items(), key=lambda x: x[1], reverse=True)[:10]:
        st.write(f"{item_name}: {qty} units sold")

def settings_page():
    st.header("⚙ Settings")
    settings = load_json(SETTINGS_FILE) or {}
    with st.form("settings_form"):
        cafe_name = st.text_input("Café Name", value=settings.get('cafe_name', 'My Café'))
        barcode_url = st.text_input("Menu URL for QR Code", value=settings.get('barcode_url', 'https://mycafe.com/menu'))
        tax_rate = st.number_input("Tax Rate (%)", min_value=0.0, max_value=100.0, value=settings.get('tax_rate', 0.10) * 100, step=0.1)
        service_charge = st.number_input("Service Charge (%)", min_value=0.0, max_value=100.0, value=settings.get('service_charge', 0.05) * 100, step=0.1)
        if st.form_submit_button("Save Settings"):
            new_settings = {
                "cafe_name": cafe_name,
                "barcode_url": barcode_url,
                "tax_rate": tax_rate / 100,
                "service_charge": service_charge / 100
            }
            save_json(SETTINGS_FILE, new_settings)
            st.success("Settings saved")
            st.rerun()
    st.subheader("Data Management")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Export Menu Data"):
            menu = load_json(MENU_FILE)
            st.download_button("Download Menu JSON", json.dumps(menu, indent=2), "menu_data.json", "application/json")
    with col2:
        if st.button("Export Orders Data"):
            orders = load_json(ORDERS_FILE)
            st.download_button("Download Orders JSON", json.dumps(orders, indent=2), "orders_data.json", "application/json")
    with col3:
        if st.button("Clear All Data"):
            if st.checkbox("I understand this will delete all data"):
                if st.button("Confirm Clear All"):
                    save_json(MENU_FILE, {"beverages": [], "food": []})
                    save_json(ORDERS_FILE, [])
                    save_json(TABLES_FILE, [{"table_number": str(i), "status": "Available"} for i in range(1, 11)])
                    save_json(USERS_FILE, [{"username": "admin", "password": "admin123", "role": "admin"},
                                           {"username": "staff", "password": "staff123", "role": "staff"}])
                    st.success("All data cleared")
                    st.rerun()

# ---------- Main ----------
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.session_state["cart"] = []

    if not st.session_state["logged_in"]:
        login_page()
        return

    user = st.session_state["user"]
    st.sidebar.title(f"Logged in as: {user['username']} ({user['role']})")
    menu_opts = ["Dashboard", "Menu Management", "Order Management", "Sales Analytics", "Table Management", "Settings", "Logout"] \
        if user["role"] == "admin" \
        else ["Dashboard", "Order Management", "Table Management", "Logout"]
    choice = st.sidebar.selectbox("Navigation", menu_opts)
    if choice == "Logout":
        for k in ("logged_in", "user", "cart"):
            st.session_state.pop(k, None)
        st.rerun()
    elif choice == "Dashboard":
        dashboard_page()
    elif choice == "Menu Management":
        menu_management_page() if user["role"] == "admin" else st.warning("Admin only")
    elif choice == "Order Management":
        order_management_page()
    elif choice == "Sales Analytics":
        sales_analytics_page() if user["role"] == "admin" else st.warning("Admin only")
    elif choice == "Table Management":
        table_management_page()
    elif choice == "Settings":
        settings_page() if user["role"] == "admin" else st.warning("Admin only")

if __name__ == "__main__":
    if 'cart' not in st.session_state: 
        st.session_state['cart'] = []
    main()
 


