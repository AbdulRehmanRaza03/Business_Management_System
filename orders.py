import streamlit as st
from utils.helpers import load_json, save_json, generate_id, now_str, today_str, format_currency, get_tax_rate, get_tax_label, get_currency_symbol
from utils.calculations import calc_order_totals

def show():
    mode = st.session_state.store_mode
    currency = get_currency_symbol(mode)
    tax_rate = get_tax_rate(mode)
    tax_label = get_tax_label(mode)

    st.markdown("# 🧾 Order Management")
    st.markdown("*Create orders, generate invoices, track sales*")
    st.markdown("---")

    tab1, tab2 = st.tabs(["➕ New Order", "📋 Order History"])

    products = load_json("products.json")
    orders = load_json("orders.json")
    customers = load_json("customers.json")

    # ── Tab 1: New Order ─────────────────────────────────────────────────────
    with tab1:
        in_stock = [p for p in products if p["stock"] > 0]
        if not in_stock:
            st.error("❌ No products in stock. Add products first.")
            return

        st.markdown('<div class="section-header">🛒 Create New Order</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            # Customer selection
            cust_names = ["New Customer"] + [c["name"] for c in customers]
            selected_cust = st.selectbox("👤 Customer", cust_names)

            if selected_cust == "New Customer":
                cust_name = st.text_input("Customer Name *")
                cust_phone = st.text_input("Phone")
                cust_email = st.text_input("Email")
            else:
                cust_obj = next(c for c in customers if c["name"] == selected_cust)
                cust_name = selected_cust
                st.markdown(f"""
                <div class="alert-info">
                    📱 {cust_obj['phone']} &nbsp;|&nbsp; ✉️ {cust_obj['email']}<br>
                    🛍️ Previous orders: <b>{cust_obj['total_orders']}</b> &nbsp;|&nbsp;
                    Total spent: <b>{format_currency(cust_obj['total_spent'], mode)}</b>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            prod_options = {f"{p['name']} (Stock: {p['stock']})": p for p in in_stock}
            selected_prod_key = st.selectbox("📦 Product", list(prod_options.keys()))
            selected_prod = prod_options[selected_prod_key]

            quantity = st.number_input("Quantity", min_value=1, max_value=selected_prod["stock"], value=1)
            discount = st.number_input(f"Discount ({currency})", min_value=0.0, value=0.0)

        # Live calculation
        totals = calc_order_totals(selected_prod["selling_price"], quantity, discount, tax_rate)

        st.markdown("---")
        st.markdown('<div class="section-header">🧮 Order Summary</div>', unsafe_allow_html=True)

        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Subtotal", format_currency(totals["subtotal"], mode))
        s2.metric("Discount", f"- {format_currency(discount, mode)}")
        s3.metric(tax_label, format_currency(totals["tax_amount"], mode))
        s4.metric("💰 Final Amount", format_currency(totals["final_amount"], mode))

        st.markdown("---")

        if st.button("✅ Confirm Order & Generate Invoice", type="primary", use_container_width=True):
            if selected_cust == "New Customer" and not cust_name:
                st.error("Please enter customer name.")
            else:
                # Handle new customer
                if selected_cust == "New Customer":
                    custs = load_json("customers.json")
                    cust_id = generate_id("CUS")
                    custs.append({
                        "id": cust_id,
                        "name": cust_name,
                        "phone": cust_phone if 'cust_phone' in dir() else "",
                        "email": cust_email if 'cust_email' in dir() else "",
                        "city": "",
                        "date_joined": today_str(),
                        "total_orders": 1,
                        "total_spent": totals["final_amount"]
                    })
                    save_json("customers.json", custs)
                else:
                    cust_id = cust_obj["id"]
                    # Update customer stats
                    custs = load_json("customers.json")
                    for c in custs:
                        if c["id"] == cust_id:
                            c["total_orders"] += 1
                            c["total_spent"] += totals["final_amount"]
                    save_json("customers.json", custs)

                # Create order
                order_id = generate_id("ORD")
                new_order = {
                    "order_id": order_id,
                    "customer_id": cust_id,
                    "customer_name": cust_name,
                    "product_id": selected_prod["id"],
                    "product_name": selected_prod["name"],
                    "category": selected_prod["category"],
                    "quantity": quantity,
                    "unit_price": selected_prod["selling_price"],
                    "discount": discount,
                    "tax_rate": tax_rate,
                    "tax_amount": totals["tax_amount"],
                    "subtotal": totals["subtotal"],
                    "final_amount": totals["final_amount"],
                    "store_mode": mode,
                    "date": today_str(),
                    "timestamp": now_str(),
                    "status": "completed"
                }
                orders_data = load_json("orders.json")
                orders_data.append(new_order)
                save_json("orders.json", orders_data)

                # Update stock
                prods = load_json("products.json")
                for p in prods:
                    if p["id"] == selected_prod["id"]:
                        p["stock"] -= quantity
                save_json("products.json", prods)

                # Show invoice
                st.success(f"✅ Order {order_id} created!")
                st.balloons()

                st.markdown(f"""
                <div class="kpi-card" style="text-align:left;max-width:600px;margin:16px auto;">
                    <div style="text-align:center;margin-bottom:16px;">
                        <div style="font-size:1.5rem;">🧾 INVOICE</div>
                        <div style="color:#9ca3af;font-size:.85rem;">{now_str()}</div>
                    </div>
                    <hr style="border-color:#2e3347;">
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px;">
                        <div><span style="color:#9ca3af;">Order ID:</span> <b style="color:#7c83fd;">{order_id}</b></div>
                        <div><span style="color:#9ca3af;">Customer:</span> <b>{cust_name}</b></div>
                        <div><span style="color:#9ca3af;">Product:</span> <b>{selected_prod['name']}</b></div>
                        <div><span style="color:#9ca3af;">Quantity:</span> <b>{quantity}</b></div>
                        <div><span style="color:#9ca3af;">Unit Price:</span> <b>{format_currency(selected_prod['selling_price'], mode)}</b></div>
                        <div><span style="color:#9ca3af;">Mode:</span> <b>{"🇵🇰 National" if mode=="national" else "🌍 International"}</b></div>
                    </div>
                    <hr style="border-color:#2e3347;">
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;">
                        <div style="color:#9ca3af;">Subtotal:</div><div>{format_currency(totals['subtotal'], mode)}</div>
                        <div style="color:#9ca3af;">Discount:</div><div style="color:#ef4444;">- {format_currency(discount, mode)}</div>
                        <div style="color:#9ca3af;">{tax_label}:</div><div>{format_currency(totals['tax_amount'], mode)}</div>
                    </div>
                    <hr style="border-color:#2e3347;">
                    <div style="text-align:right;font-size:1.3rem;font-weight:700;color:#10b981;">
                        Total: {format_currency(totals['final_amount'], mode)}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Tab 2: History ───────────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-header">📋 Order History</div>', unsafe_allow_html=True)

        mode_orders = [o for o in orders if o.get("store_mode") == mode]
        mode_orders.sort(key=lambda x: x["date"], reverse=True)

        if not mode_orders:
            st.info("No orders yet in this store mode.")
            return

        # Summary stats
        total = sum(o["final_amount"] for o in mode_orders)
        st.markdown(f"""
        <div style="display:flex;gap:16px;margin-bottom:16px;">
            <div class="kpi-card" style="flex:1;text-align:center;">
                <div class="kpi-value">{len(mode_orders)}</div>
                <div class="kpi-label">Total Orders</div>
            </div>
            <div class="kpi-card" style="flex:2;text-align:center;">
                <div class="kpi-value" style="color:#10b981;">{format_currency(total, mode)}</div>
                <div class="kpi-label">Total Revenue</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <table class="styled-table">
        <thead><tr>
            <th>Order ID</th><th>Customer</th><th>Product</th>
            <th>Qty</th><th>Discount</th><th>Tax</th><th>Final</th><th>Date</th>
        </tr></thead><tbody>
        """, unsafe_allow_html=True)

        for o in mode_orders:
            st.markdown(f"""
            <tr>
                <td><span class="badge badge-blue">{o['order_id']}</span></td>
                <td>{o['customer_name']}</td>
                <td>{o['product_name']}</td>
                <td>{o['quantity']}</td>
                <td style="color:#ef4444;">- {format_currency(o['discount'], mode)}</td>
                <td style="color:#f59e0b;">{format_currency(o['tax_amount'], mode)}</td>
                <td style="color:#10b981;font-weight:600;">{format_currency(o['final_amount'], mode)}</td>
                <td>{o['date']}</td>
            </tr>
            """, unsafe_allow_html=True)

        st.markdown("</tbody></table>", unsafe_allow_html=True)
