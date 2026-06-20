import streamlit as st
from utils.helpers import load_json, save_json, generate_id, today_str, format_currency

CATEGORIES = ["Electronics", "Clothing", "Footwear", "Home Appliances", "Food & Beverages", "Sports", "Books", "Other"]

def show():
    mode = st.session_state.store_mode
    st.markdown("# 📦 Product Management")
    st.markdown("*Add, update, search, and manage your inventory*")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📋 All Products", "➕ Add Product", "🔍 Search"])

    products = load_json("products.json")

    # ── Tab 1: View All ──────────────────────────────────────────────────────
    with tab1:
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            cat_filter = st.selectbox("Filter by Category", ["All"] + CATEGORIES)
        with col_b:
            stock_filter = st.selectbox("Filter by Stock", ["All", "In Stock", "Low Stock (<5)", "Out of Stock"])
        with col_c:
            sort_by = st.selectbox("Sort By", ["Name", "Price (High→Low)", "Stock (Low→High)"])

        filtered = products[:]
        if cat_filter != "All":
            filtered = [p for p in filtered if p["category"] == cat_filter]
        if stock_filter == "In Stock":
            filtered = [p for p in filtered if p["stock"] > 5]
        elif stock_filter == "Low Stock (<5)":
            filtered = [p for p in filtered if 0 < p["stock"] < 5]
        elif stock_filter == "Out of Stock":
            filtered = [p for p in filtered if p["stock"] == 0]

        if sort_by == "Price (High→Low)":
            filtered.sort(key=lambda x: x["selling_price"], reverse=True)
        elif sort_by == "Stock (Low→High)":
            filtered.sort(key=lambda x: x["stock"])
        else:
            filtered.sort(key=lambda x: x["name"])

        st.markdown(f"**Showing {len(filtered)} of {len(products)} products**")
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        if not filtered:
            st.info("No products match the filter.")
        else:
            for p in filtered:
                with st.expander(f"**{p['name']}** | {p['category']} | Stock: {p['stock']}", expanded=False):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Product ID", p["id"])
                    c2.metric("Purchase Price", format_currency(p["purchase_price"], mode))
                    c3.metric("Selling Price", format_currency(p["selling_price"], mode))
                    margin = round((p["selling_price"] - p["purchase_price"]) / p["selling_price"] * 100, 1)
                    c4.metric("Margin", f"{margin}%")

                    col_info, col_actions = st.columns([3, 1])
                    with col_info:
                        st.markdown(f"""
                        <table class="styled-table">
                        <tr><th>Field</th><th>Value</th></tr>
                        <tr><td>Supplier</td><td>{p['supplier']}</td></tr>
                        <tr><td>Date Added</td><td>{p['date_added']}</td></tr>
                        <tr><td>Stock Status</td><td>{'🔴 Out of Stock' if p['stock']==0 else '🟡 Low Stock' if p['stock']<5 else '🟢 In Stock'}</td></tr>
                        </table>
                        """, unsafe_allow_html=True)

                    with col_actions:
                        st.markdown("**Actions**")
                        new_stock = st.number_input("Update Stock", value=p["stock"], min_value=0, key=f"stock_{p['id']}")
                        new_price = st.number_input("Update Selling Price", value=float(p["selling_price"]), min_value=0.0, key=f"price_{p['id']}")

                        if st.button("💾 Update", key=f"upd_{p['id']}", use_container_width=True):
                            for prod in products:
                                if prod["id"] == p["id"]:
                                    prod["stock"] = new_stock
                                    prod["selling_price"] = new_price
                            save_json("products.json", products)
                            st.success("✅ Product updated!")
                            st.rerun()

                        if st.button("🗑️ Delete", key=f"del_{p['id']}", use_container_width=True):
                            products = [x for x in products if x["id"] != p["id"]]
                            save_json("products.json", products)
                            st.warning("⚠️ Product deleted.")
                            st.rerun()

    # ── Tab 2: Add Product ───────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-header">➕ Add New Product</div>', unsafe_allow_html=True)

        with st.form("add_product_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Product Name *", placeholder="e.g. iPhone 15 Pro")
                category = st.selectbox("Category *", CATEGORIES)
                purchase_price = st.number_input("Purchase Price *", min_value=0.0, value=0.0)
                selling_price = st.number_input("Selling Price *", min_value=0.0, value=0.0)
            with c2:
                stock = st.number_input("Stock Quantity *", min_value=0, value=0)
                supplier = st.text_input("Supplier Name *", placeholder="e.g. Apple Distributors")
                st.markdown(f"""
                <div class="alert-info" style="margin-top:20px;">
                    <b>Current Mode:</b> {mode.title()} Store<br>
                    <b>Currency:</b> {'PKR' if mode == 'national' else 'USD'}
                </div>
                """, unsafe_allow_html=True)

            submitted = st.form_submit_button("✅ Add Product", use_container_width=True, type="primary")

            if submitted:
                if not name or selling_price <= 0 or not supplier:
                    st.error("❌ Please fill all required fields with valid values.")
                elif selling_price < purchase_price:
                    st.error("❌ Selling price must be >= purchase price.")
                else:
                    products = load_json("products.json")
                    new_id = generate_id("PRD")
                    new_prod = {
                        "id": new_id,
                        "name": name,
                        "category": category,
                        "purchase_price": purchase_price,
                        "selling_price": selling_price,
                        "stock": stock,
                        "supplier": supplier,
                        "date_added": today_str(),
                        "store_mode": mode
                    }
                    products.append(new_prod)
                    save_json("products.json", products)
                    st.success(f"✅ Product '{name}' added with ID: **{new_id}**")

    # ── Tab 3: Search ────────────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-header">🔍 Search Products</div>', unsafe_allow_html=True)
        query = st.text_input("Search by name, category, or supplier", placeholder="Type to search...")

        if query:
            q = query.lower()
            results = [p for p in products if q in p["name"].lower() or q in p["category"].lower() or q in p["supplier"].lower()]
            st.markdown(f"**Found {len(results)} result(s)**")
            for p in results:
                stock_badge = "badge-red" if p["stock"] == 0 else "badge-yellow" if p["stock"] < 5 else "badge-green"
                stock_label = "Out of Stock" if p["stock"] == 0 else "Low Stock" if p["stock"] < 5 else "In Stock"
                st.markdown(f"""
                <div class="kpi-card" style="text-align:left;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="font-weight:700;font-size:1rem;color:#e0e0e0;">{p['name']}</span>
                            <span class="badge badge-blue" style="margin-left:8px;">{p['id']}</span>
                        </div>
                        <span class="badge {stock_badge}">{stock_label} ({p['stock']})</span>
                    </div>
                    <div style="margin-top:10px;color:#9ca3af;font-size:.88rem;">
                        Category: <b style="color:#e0e0e0">{p['category']}</b> &nbsp;|&nbsp;
                        Sell: <b style="color:#7c83fd">{format_currency(p['selling_price'], mode)}</b> &nbsp;|&nbsp;
                        Buy: <b style="color:#f59e0b">{format_currency(p['purchase_price'], mode)}</b> &nbsp;|&nbsp;
                        Supplier: {p['supplier']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Start typing to search products...")
