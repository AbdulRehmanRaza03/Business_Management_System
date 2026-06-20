import streamlit as st
import plotly.graph_objects as go
from utils.helpers import load_json, save_json, generate_id, today_str, format_currency

def show():
    mode = st.session_state.store_mode

    st.markdown("# 👤 Customer Management")
    st.markdown("*Track customers, purchase history, and top spenders*")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["👥 All Customers", "➕ Add Customer", "🏆 Top Customers"])

    customers = load_json("customers.json")
    orders = load_json("orders.json")

    # ── Tab 1: All Customers ─────────────────────────────────────────────────
    with tab1:
        if not customers:
            st.info("No customers yet. Add your first customer!")
        else:
            search = st.text_input("🔍 Search customers", placeholder="Name, phone, or email...")
            filtered = customers
            if search:
                q = search.lower()
                filtered = [c for c in customers if q in c["name"].lower() or q in c.get("phone","").lower() or q in c.get("email","").lower()]

            st.markdown(f"**{len(filtered)} customer(s) found**")

            for cust in filtered:
                cust_orders = [o for o in orders if o.get("customer_id") == cust["id"] and o.get("store_mode") == mode]
                spent_mode = sum(o["final_amount"] for o in cust_orders)

                with st.expander(f"**{cust['name']}** | {cust.get('phone','N/A')} | {len(cust_orders)} orders", expanded=False):
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Customer ID", cust["id"])
                    col2.metric("Total Orders", cust["total_orders"])
                    col3.metric("Total Spent (All)", format_currency(cust["total_spent"], mode))
                    col4.metric("Spent (This Mode)", format_currency(spent_mode, mode))

                    st.markdown(f"""
                    <table class="styled-table">
                    <tr><th>Field</th><th>Value</th></tr>
                    <tr><td>📧 Email</td><td>{cust.get('email','N/A')}</td></tr>
                    <tr><td>📱 Phone</td><td>{cust.get('phone','N/A')}</td></tr>
                    <tr><td>🏙️ City</td><td>{cust.get('city','N/A')}</td></tr>
                    <tr><td>📅 Joined</td><td>{cust['date_joined']}</td></tr>
                    </table>
                    """, unsafe_allow_html=True)

                    if cust_orders:
                        st.markdown("**Purchase History (This Mode)**")
                        st.markdown("""
                        <table class="styled-table">
                        <thead><tr><th>Order ID</th><th>Product</th><th>Qty</th><th>Amount</th><th>Date</th></tr></thead><tbody>
                        """, unsafe_allow_html=True)
                        for o in sorted(cust_orders, key=lambda x: x["date"], reverse=True):
                            st.markdown(f"""
                            <tr>
                                <td><span class="badge badge-blue">{o['order_id']}</span></td>
                                <td>{o['product_name']}</td>
                                <td>{o['quantity']}</td>
                                <td style="color:#10b981;">{format_currency(o['final_amount'], mode)}</td>
                                <td>{o['date']}</td>
                            </tr>
                            """, unsafe_allow_html=True)
                        st.markdown("</tbody></table>", unsafe_allow_html=True)
                    else:
                        st.info("No orders in this store mode.")

                    if st.button("🗑️ Delete Customer", key=f"del_cust_{cust['id']}"):
                        custs = [c for c in customers if c["id"] != cust["id"]]
                        save_json("customers.json", custs)
                        st.warning("Customer deleted.")
                        st.rerun()

    # ── Tab 2: Add Customer ──────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-header">➕ Add New Customer</div>', unsafe_allow_html=True)

        with st.form("add_customer_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Full Name *")
                phone = st.text_input("Phone Number")
                email = st.text_input("Email Address")
            with c2:
                city = st.text_input("City")
                st.markdown("""
                <div class="alert-info" style="margin-top:20px;">
                    Customer will be added to the system and can be selected during order creation.
                </div>
                """, unsafe_allow_html=True)

            submitted = st.form_submit_button("✅ Add Customer", use_container_width=True, type="primary")

            if submitted:
                if not name:
                    st.error("Customer name is required.")
                else:
                    custs = load_json("customers.json")
                    cust_id = generate_id("CUS")
                    custs.append({
                        "id": cust_id,
                        "name": name,
                        "phone": phone,
                        "email": email,
                        "city": city,
                        "date_joined": today_str(),
                        "total_orders": 0,
                        "total_spent": 0
                    })
                    save_json("customers.json", custs)
                    st.success(f"✅ Customer '{name}' added with ID: **{cust_id}**")

    # ── Tab 3: Top Customers ─────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-header">🏆 Top Customers by Spending</div>', unsafe_allow_html=True)

        if not customers:
            st.info("No customers yet.")
            return

        # Calculate per-mode spending
        cust_mode_spend = []
        for c in customers:
            c_orders = [o for o in orders if o.get("customer_id") == c["id"] and o.get("store_mode") == mode]
            spent = sum(o["final_amount"] for o in c_orders)
            if spent > 0:
                cust_mode_spend.append({"name": c["name"], "spent": spent, "orders": len(c_orders)})

        cust_mode_spend.sort(key=lambda x: x["spent"], reverse=True)

        if not cust_mode_spend:
            st.info("No spending data for this store mode.")
            return

        # Bar chart
        names = [c["name"] for c in cust_mode_spend]
        vals = [c["spent"] for c in cust_mode_spend]
        fig = go.Figure(go.Bar(
            x=names, y=vals,
            marker=dict(color=vals, colorscale=[[0,"#3b4fd8"],[1,"#7c83fd"]], showscale=False),
            text=[format_currency(v, mode) for v in vals],
            textposition="outside"
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9ca3af"),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"),
            yaxis=dict(gridcolor="#2e3347"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)

        # Medals
        medals = ["🥇", "🥈", "🥉"]
        for i, c in enumerate(cust_mode_spend[:5]):
            medal = medals[i] if i < 3 else f"#{i+1}"
            st.markdown(f"""
            <div class="kpi-card" style="text-align:left;display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <span style="font-size:1.2rem;">{medal}</span>
                    <span style="font-weight:700;color:#e0e0e0;margin-left:8px;">{c['name']}</span>
                </div>
                <div>
                    <span style="color:#10b981;font-weight:700;font-size:1.1rem;">{format_currency(c['spent'], mode)}</span>
                    <span style="color:#9ca3af;font-size:.8rem;margin-left:8px;">({c['orders']} orders)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
