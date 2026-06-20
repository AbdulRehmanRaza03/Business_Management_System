import streamlit as st
import plotly.graph_objects as go
from utils.helpers import load_json, save_json, format_currency

def show():
    mode = st.session_state.store_mode

    st.markdown("# 📉 Inventory Alert System")
    st.markdown("*Monitor stock levels, get alerts, manage reorders*")
    st.markdown("---")

    products = load_json("products.json")

    low_threshold = st.slider("⚙️ Low Stock Threshold", 1, 20, 5)
    overstock_threshold = st.slider("⚙️ Overstock Threshold", 50, 200, 100)

    out_of_stock = [p for p in products if p["stock"] == 0]
    low_stock = [p for p in products if 0 < p["stock"] < low_threshold]
    healthy = [p for p in products if low_threshold <= p["stock"] <= overstock_threshold]
    overstock = [p for p in products if p["stock"] > overstock_threshold]

    # ── Alert KPIs ───────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div style="font-size:2rem;">🔴</div>
            <div class="kpi-value" style="color:#ef4444;">{len(out_of_stock)}</div>
            <div class="kpi-label">Out of Stock</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div style="font-size:2rem;">🟡</div>
            <div class="kpi-value" style="color:#f59e0b;">{len(low_stock)}</div>
            <div class="kpi-label">Low Stock</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div style="font-size:2rem;">🟢</div>
            <div class="kpi-value" style="color:#10b981;">{len(healthy)}</div>
            <div class="kpi-label">Healthy Stock</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div style="font-size:2rem;">🔵</div>
            <div class="kpi-value" style="color:#3b82f6;">{len(overstock)}</div>
            <div class="kpi-label">Overstock</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Stock Bar Chart ──────────────────────────────────────────────────────
    st.markdown('<div class="section-header">📊 Stock Level Overview</div>', unsafe_allow_html=True)

    colors = []
    for p in products:
        if p["stock"] == 0:
            colors.append("#ef4444")
        elif p["stock"] < low_threshold:
            colors.append("#f59e0b")
        elif p["stock"] > overstock_threshold:
            colors.append("#3b82f6")
        else:
            colors.append("#10b981")

    fig = go.Figure(go.Bar(
        x=[p["name"][:15] for p in products],
        y=[p["stock"] for p in products],
        marker_color=colors,
        text=[str(p["stock"]) for p in products],
        textposition="outside"
    ))
    fig.add_hline(y=low_threshold, line_dash="dash", line_color="#f59e0b",
                  annotation_text=f"Low ({low_threshold})", annotation_position="right")
    fig.add_hline(y=overstock_threshold, line_dash="dash", line_color="#3b82f6",
                  annotation_text=f"Overstock ({overstock_threshold})", annotation_position="right")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#9ca3af"),
        xaxis=dict(gridcolor="rgba(0,0,0,0)", tickangle=-30),
        yaxis=dict(gridcolor="#2e3347"),
        margin=dict(l=0,r=0,t=10,b=80),
        height=320
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Critical Alerts ──────────────────────────────────────────────────────
    if out_of_stock:
        st.markdown('<div class="section-header">🔴 Out of Stock — Immediate Action Required</div>', unsafe_allow_html=True)
        for p in out_of_stock:
            st.markdown(f"""
            <div class="alert-danger">
                <b>🔴 {p['name']}</b> &nbsp;|&nbsp; Category: {p['category']}
                &nbsp;|&nbsp; Supplier: {p['supplier']}
                &nbsp;|&nbsp; <span style="color:#ef4444;">STOCK: 0 — OUT OF STOCK</span>
            </div>
            """, unsafe_allow_html=True)

    if low_stock:
        st.markdown('<div class="section-header">🟡 Low Stock — Reorder Soon</div>', unsafe_allow_html=True)
        for p in low_stock:
            st.markdown(f"""
            <div class="alert-warning">
                <b>🟡 {p['name']}</b> &nbsp;|&nbsp; Category: {p['category']}
                &nbsp;|&nbsp; Supplier: {p['supplier']}
                &nbsp;|&nbsp; <span style="color:#f59e0b;">Stock: {p['stock']} units</span>
            </div>
            """, unsafe_allow_html=True)

    if overstock:
        st.markdown('<div class="section-header">🔵 Overstock Warning</div>', unsafe_allow_html=True)
        for p in overstock:
            st.markdown(f"""
            <div class="alert-info">
                <b>🔵 {p['name']}</b> &nbsp;|&nbsp; Category: {p['category']}
                &nbsp;|&nbsp; <span style="color:#3b82f6;">Stock: {p['stock']} units — OVERSTOCK</span>
                &nbsp;|&nbsp; Consider promotions or bulk discounts
            </div>
            """, unsafe_allow_html=True)

    if not out_of_stock and not low_stock:
        st.markdown('<div class="alert-success">✅ All products have healthy stock levels!</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Quick Restock ────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">🔄 Quick Stock Update</div>', unsafe_allow_html=True)

    needs_restock = out_of_stock + low_stock
    if needs_restock:
        with st.form("restock_form"):
            prod_sel = st.selectbox("Select Product to Restock",
                                    [p["name"] for p in needs_restock])
            add_qty = st.number_input("Quantity to Add", min_value=1, value=10)
            col_btn, _ = st.columns([1, 3])
            if st.form_submit_button("📦 Update Stock", type="primary"):
                prods = load_json("products.json")
                for p in prods:
                    if p["name"] == prod_sel:
                        old = p["stock"]
                        p["stock"] += add_qty
                        save_json("products.json", prods)
                        st.success(f"✅ {prod_sel}: stock updated from {old} → {p['stock']}")
                        st.rerun()
    else:
        st.info("No products need restocking right now.")

    st.markdown("---")

    # ── Full Inventory Table ─────────────────────────────────────────────────
    st.markdown('<div class="section-header">📋 Complete Inventory Status</div>', unsafe_allow_html=True)

    st.markdown("""
    <table class="styled-table">
    <thead><tr>
        <th>ID</th><th>Product</th><th>Category</th>
        <th>Stock</th><th>Buy Price</th><th>Sell Price</th><th>Status</th>
    </tr></thead><tbody>
    """, unsafe_allow_html=True)

    sorted_prods = sorted(products, key=lambda x: x["stock"])
    for p in sorted_prods:
        if p["stock"] == 0:
            badge = "badge-red"; status = "Out of Stock"
        elif p["stock"] < low_threshold:
            badge = "badge-yellow"; status = f"Low ({p['stock']})"
        elif p["stock"] > overstock_threshold:
            badge = "badge-blue"; status = f"Overstock ({p['stock']})"
        else:
            badge = "badge-green"; status = f"OK ({p['stock']})"

        st.markdown(f"""
        <tr>
            <td><span class="badge badge-blue">{p['id']}</span></td>
            <td>{p['name']}</td>
            <td>{p['category']}</td>
            <td style="font-weight:700;">{p['stock']}</td>
            <td>{format_currency(p['purchase_price'], mode)}</td>
            <td>{format_currency(p['selling_price'], mode)}</td>
            <td><span class="badge {badge}">{status}</span></td>
        </tr>
        """, unsafe_allow_html=True)

    st.markdown("</tbody></table>", unsafe_allow_html=True)
