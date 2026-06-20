import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.helpers import format_currency, load_json
from utils.calculations import get_kpis, get_sales_over_time, get_top_products, get_category_revenue, generate_insights

def show():
    mode = st.session_state.store_mode
    flag = "🇵🇰" if mode == "national" else "🌍"
    currency = "PKR" if mode == "national" else "USD"

    st.markdown(f"# {flag} Dashboard — {mode.title()} Store")
    st.markdown(f"*Real-time business intelligence · {currency} currency*")
    st.markdown("---")

    with st.spinner("Loading KPIs..."):
        kpis = get_kpis(mode)

    # ── KPI Row ──────────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    cards = [
        (c1, "💰", "Total Revenue", format_currency(kpis["total_revenue"], mode), "#7c83fd"),
        (c2, "📦", "Total Orders", str(kpis["total_orders"]), "#10b981"),
        (c3, "💵", "Net Profit", format_currency(kpis["total_profit"], mode), "#f59e0b"),
        (c4, "📈", "Profit Margin", f"{kpis['profit_margin']}%", "#3b82f6"),
        (c5, "🏷️", "Products", str(kpis["total_products"]), "#8b5cf6"),
        (c6, "⚠️", "Low Stock", str(kpis["low_stock_count"]), "#ef4444"),
    ]
    for col, icon, label, value, color in cards:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div style="font-size:1.6rem;">{icon}</div>
                <div class="kpi-value" style="color:{color};">{value}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Charts Row ───────────────────────────────────────────────────────────
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="section-header">📈 Sales Over Time</div>', unsafe_allow_html=True)
        sales_data = get_sales_over_time(mode)
        if sales_data:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(sales_data.keys()),
                y=list(sales_data.values()),
                fill="tozeroy",
                line=dict(color="#7c83fd", width=2.5),
                fillcolor="rgba(124,131,253,0.15)",
                mode="lines+markers",
                marker=dict(size=7, color="#7c83fd"),
                name="Revenue"
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9ca3af"),
                xaxis=dict(gridcolor="#2e3347", showline=False),
                yaxis=dict(gridcolor="#2e3347", showline=False),
                margin=dict(l=0, r=0, t=10, b=0),
                height=260,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sales data yet.")

    with col_right:
        st.markdown('<div class="section-header">🏆 Top Products</div>', unsafe_allow_html=True)
        top_prods = get_top_products(mode, 5)
        if top_prods:
            names = [t[0][:20] for t in top_prods]
            vals = [t[1] for t in top_prods]
            fig2 = go.Figure(go.Bar(
                x=vals, y=names, orientation="h",
                marker=dict(
                    color=vals,
                    colorscale=[[0,"#3b4fd8"],[1,"#7c83fd"]],
                    showscale=False
                )
            ))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9ca3af"),
                xaxis=dict(gridcolor="#2e3347"),
                yaxis=dict(gridcolor="rgba(0,0,0,0)"),
                margin=dict(l=0, r=0, t=10, b=0),
                height=260
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No data yet.")

    st.markdown("---")

    # ── Row 2 ────────────────────────────────────────────────────────────────
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-header">🗂️ Category Revenue</div>', unsafe_allow_html=True)
        cat_rev = get_category_revenue(mode)
        if cat_rev:
            fig3 = go.Figure(data=[go.Pie(
                labels=list(cat_rev.keys()),
                values=list(cat_rev.values()),
                hole=0.45,
                marker=dict(colors=["#7c83fd","#10b981","#f59e0b","#3b82f6","#8b5cf6","#ef4444"])
            )])
            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9ca3af"),
                margin=dict(l=0, r=0, t=10, b=0),
                height=260,
                showlegend=True,
                legend=dict(font=dict(size=11))
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No data yet.")

    with col_b:
        st.markdown('<div class="section-header">🧠 Business Insights</div>', unsafe_allow_html=True)
        insights = generate_insights(mode)
        for insight in insights:
            st.markdown(f"""<div class="alert-info">{insight}</div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Quick Stats ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">📋 Recent Orders</div>', unsafe_allow_html=True)
    orders = load_json("orders.json")
    mode_orders = [o for o in orders if o.get("store_mode") == mode]
    recent = sorted(mode_orders, key=lambda x: x["date"], reverse=True)[:5]

    if recent:
        st.markdown("""
        <table class="styled-table">
        <thead><tr>
            <th>Order ID</th><th>Customer</th><th>Product</th>
            <th>Qty</th><th>Amount</th><th>Date</th>
        </tr></thead><tbody>
        """, unsafe_allow_html=True)
        for o in recent:
            amt = format_currency(o["final_amount"], mode)
            st.markdown(f"""
            <tr>
                <td><span class="badge badge-blue">{o['order_id']}</span></td>
                <td>{o['customer_name']}</td>
                <td>{o['product_name']}</td>
                <td>{o['quantity']}</td>
                <td style="color:#10b981;font-weight:600;">{amt}</td>
                <td>{o['date']}</td>
            </tr>
            """, unsafe_allow_html=True)
        st.markdown("</tbody></table>", unsafe_allow_html=True)
    else:
        st.info("No orders in this store mode yet.")
