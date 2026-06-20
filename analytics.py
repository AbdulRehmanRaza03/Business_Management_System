import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.helpers import load_json, format_currency
from utils.calculations import (
    get_kpis, get_sales_over_time, get_top_products,
    get_category_revenue, get_stock_distribution, get_profit_by_product
)

def show():
    mode = st.session_state.store_mode

    st.markdown("# 📊 Business Analytics")
    st.markdown("*Deep insights, trends, and performance metrics*")
    st.markdown("---")

    kpis = get_kpis(mode)

    # ── P&L Summary ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">💰 Profit & Loss Summary</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", format_currency(kpis["total_revenue"], mode))
    c2.metric("Total Cost", format_currency(kpis["total_cost"], mode))
    c3.metric("Net Profit", format_currency(kpis["total_profit"], mode),
              delta=f"{kpis['profit_margin']}% margin")
    c4.metric("Profit Margin", f"{kpis['profit_margin']}%",
              delta="Healthy" if kpis["profit_margin"] > 20 else "Low")

    # P&L bar
    fig_pl = go.Figure()
    fig_pl.add_trace(go.Bar(name="Revenue", x=["P&L"], y=[kpis["total_revenue"]], marker_color="#7c83fd"))
    fig_pl.add_trace(go.Bar(name="Cost", x=["P&L"], y=[kpis["total_cost"]], marker_color="#ef4444"))
    fig_pl.add_trace(go.Bar(name="Profit", x=["P&L"], y=[kpis["total_profit"]], marker_color="#10b981"))
    fig_pl.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#9ca3af"),
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(gridcolor="#2e3347"),
        legend=dict(font=dict(size=11)),
        margin=dict(l=0,r=0,t=10,b=0),
        height=250
    )
    st.plotly_chart(fig_pl, use_container_width=True)

    st.markdown("---")

    # ── Charts Grid ───────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">📈 Monthly Revenue Trend</div>', unsafe_allow_html=True)
        sales_data = get_sales_over_time(mode)
        if sales_data:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(sales_data.keys()),
                y=list(sales_data.values()),
                fill="tozeroy",
                line=dict(color="#7c83fd", width=2.5),
                fillcolor="rgba(124,131,253,0.12)",
                mode="lines+markers+text",
                marker=dict(size=8, color="#7c83fd"),
                text=[format_currency(v, mode) for v in sales_data.values()],
                textposition="top center",
                textfont=dict(size=9)
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9ca3af"),
                xaxis=dict(gridcolor="#2e3347"),
                yaxis=dict(gridcolor="#2e3347"),
                margin=dict(l=0,r=0,t=20,b=0),
                height=280, showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data.")

    with col2:
        st.markdown('<div class="section-header">🏆 Top Products Revenue</div>', unsafe_allow_html=True)
        top_prods = get_top_products(mode, 8)
        if top_prods:
            names = [t[0][:18] for t in top_prods]
            vals = [t[1] for t in top_prods]
            fig2 = go.Figure(go.Bar(
                x=vals, y=names, orientation="h",
                marker=dict(color=vals, colorscale=[[0,"#3b4fd8"],[1,"#a78bfa"]], showscale=False),
                text=[format_currency(v, mode) for v in vals],
                textposition="outside"
            ))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9ca3af"),
                xaxis=dict(gridcolor="#2e3347"),
                yaxis=dict(gridcolor="rgba(0,0,0,0)"),
                margin=dict(l=0,r=0,t=10,b=0),
                height=280
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No data.")

    st.markdown("---")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">🗂️ Category Revenue Breakdown</div>', unsafe_allow_html=True)
        cat_rev = get_category_revenue(mode)
        if cat_rev:
            fig3 = go.Figure(data=[go.Pie(
                labels=list(cat_rev.keys()),
                values=list(cat_rev.values()),
                hole=0.4,
                marker=dict(colors=["#7c83fd","#10b981","#f59e0b","#3b82f6","#8b5cf6","#ef4444","#14b8a6"])
            )])
            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9ca3af"),
                margin=dict(l=0,r=0,t=10,b=0),
                height=300,
                legend=dict(font=dict(size=10))
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No data.")

    with col4:
        st.markdown('<div class="section-header">📦 Stock Distribution by Category</div>', unsafe_allow_html=True)
        stock_dist = get_stock_distribution()
        if stock_dist:
            fig4 = go.Figure(data=[go.Bar(
                x=list(stock_dist.keys()),
                y=list(stock_dist.values()),
                marker=dict(color=list(stock_dist.values()), colorscale=[[0,"#1d4ed8"],[1,"#7c83fd"]]),
                text=list(stock_dist.values()),
                textposition="outside"
            )])
            fig4.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9ca3af"),
                xaxis=dict(gridcolor="rgba(0,0,0,0)"),
                yaxis=dict(gridcolor="#2e3347"),
                margin=dict(l=0,r=0,t=10,b=0),
                height=300
            )
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("No data.")

    st.markdown("---")

    # ── Profit per Product ───────────────────────────────────────────────────
    st.markdown('<div class="section-header">💹 Profit vs Cost per Product</div>', unsafe_allow_html=True)
    profit_data = get_profit_by_product(mode)
    if profit_data:
        prod_names = list(profit_data.keys())
        revenues = [profit_data[p]["revenue"] for p in prod_names]
        costs = [profit_data[p]["cost"] for p in prod_names]
        profits = [profit_data[p]["profit"] for p in prod_names]

        fig5 = go.Figure()
        fig5.add_trace(go.Bar(name="Revenue", x=prod_names, y=revenues, marker_color="#7c83fd"))
        fig5.add_trace(go.Bar(name="Cost", x=prod_names, y=costs, marker_color="#ef4444"))
        fig5.add_trace(go.Bar(name="Profit", x=prod_names, y=profits, marker_color="#10b981"))
        fig5.update_layout(
            barmode="group",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9ca3af"),
            xaxis=dict(gridcolor="rgba(0,0,0,0)", tickangle=-30),
            yaxis=dict(gridcolor="#2e3347"),
            legend=dict(font=dict(size=11)),
            margin=dict(l=0,r=0,t=10,b=80),
            height=320
        )
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.info("No order data available for profit analysis.")

    # ── National vs International ────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-header">🌍 National vs International Comparison</div>', unsafe_allow_html=True)

    nat_kpi = get_kpis("national")
    int_kpi = get_kpis("international")

    ca, cb = st.columns(2)
    with ca:
        st.markdown("""<div class="kpi-card">
            <div style="font-size:1.5rem;">🇵🇰 National Store</div>
        </div>""", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("Revenue (PKR)", f"{nat_kpi['total_revenue']:,.0f}")
        m2.metric("Orders", nat_kpi["total_orders"])
        m3.metric("Margin", f"{nat_kpi['profit_margin']}%")

    with cb:
        st.markdown("""<div class="kpi-card">
            <div style="font-size:1.5rem;">🌍 International Store</div>
        </div>""", unsafe_allow_html=True)
        m4, m5, m6 = st.columns(3)
        m4.metric("Revenue (USD)", f"{int_kpi['total_revenue']:,.2f}")
        m5.metric("Orders", int_kpi["total_orders"])
        m6.metric("Margin", f"{int_kpi['profit_margin']}%")

    fig6 = go.Figure()
    categories = ["Revenue", "Orders", "Profit"]
    nat_vals = [nat_kpi["total_revenue"], nat_kpi["total_orders"] * 10000, nat_kpi["total_profit"]]
    int_vals = [int_kpi["total_revenue"], int_kpi["total_orders"] * 10000, int_kpi["total_profit"]]
    fig6.add_trace(go.Bar(name="🇵🇰 National (PKR)", x=categories, y=nat_vals, marker_color="#7c83fd"))
    fig6.add_trace(go.Bar(name="🌍 International (USD)", x=categories, y=int_vals, marker_color="#10b981"))
    fig6.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#9ca3af"),
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(gridcolor="#2e3347"),
        legend=dict(font=dict(size=11)),
        margin=dict(l=0,r=0,t=10,b=0),
        height=260
    )
    st.plotly_chart(fig6, use_container_width=True)
    st.caption("*Note: Orders scaled ×10,000 for visual comparison across currency scales*")
