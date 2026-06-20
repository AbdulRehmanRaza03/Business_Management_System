from utils.helpers import load_json

def calc_order_totals(unit_price, quantity, discount, tax_rate):
    subtotal = unit_price * quantity
    after_discount = subtotal - discount
    tax_amount = after_discount * tax_rate
    final = after_discount + tax_amount
    return {
        "subtotal": subtotal,
        "after_discount": after_discount,
        "tax_amount": round(tax_amount, 2),
        "final_amount": round(final, 2)
    }

def get_kpis(store_mode):
    orders = load_json("orders.json")
    products = load_json("products.json")

    mode_orders = [o for o in orders if o.get("store_mode") == store_mode]

    total_revenue = sum(o["final_amount"] for o in mode_orders)
    total_orders = len(mode_orders)

    total_cost = 0
    for o in mode_orders:
        prod = next((p for p in products if p["id"] == o["product_id"]), None)
        if prod:
            total_cost += prod["purchase_price"] * o["quantity"]

    total_profit = total_revenue - total_cost
    profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0

    low_stock = [p for p in products if p["stock"] < 5 and p["stock"] > 0]
    out_of_stock = [p for p in products if p["stock"] == 0]
    overstock = [p for p in products if p["stock"] > 100]

    total_products = len(products)

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "total_profit": total_profit,
        "profit_margin": round(profit_margin, 1),
        "total_products": total_products,
        "low_stock_count": len(low_stock),
        "out_of_stock_count": len(out_of_stock),
        "overstock_count": len(overstock),
        "total_cost": total_cost
    }

def get_sales_over_time(store_mode):
    orders = load_json("orders.json")
    mode_orders = [o for o in orders if o.get("store_mode") == store_mode]
    sales_by_date = {}
    for o in mode_orders:
        d = o["date"][:7]  # YYYY-MM
        sales_by_date[d] = sales_by_date.get(d, 0) + o["final_amount"]
    return dict(sorted(sales_by_date.items()))

def get_top_products(store_mode, n=5):
    orders = load_json("orders.json")
    mode_orders = [o for o in orders if o.get("store_mode") == store_mode]
    prod_sales = {}
    for o in mode_orders:
        pname = o["product_name"]
        prod_sales[pname] = prod_sales.get(pname, 0) + o["final_amount"]
    sorted_prods = sorted(prod_sales.items(), key=lambda x: x[1], reverse=True)
    return sorted_prods[:n]

def get_category_revenue(store_mode):
    orders = load_json("orders.json")
    mode_orders = [o for o in orders if o.get("store_mode") == store_mode]
    cat_rev = {}
    for o in mode_orders:
        cat = o.get("category", "Other")
        cat_rev[cat] = cat_rev.get(cat, 0) + o["final_amount"]
    return cat_rev

def get_stock_distribution():
    products = load_json("products.json")
    cat_stock = {}
    for p in products:
        cat = p["category"]
        cat_stock[cat] = cat_stock.get(cat, 0) + p["stock"]
    return cat_stock

def get_profit_by_product(store_mode):
    orders = load_json("orders.json")
    products = load_json("products.json")
    mode_orders = [o for o in orders if o.get("store_mode") == store_mode]
    result = {}
    for o in mode_orders:
        prod = next((p for p in products if p["id"] == o["product_id"]), None)
        if prod:
            cost = prod["purchase_price"] * o["quantity"]
            profit = o["final_amount"] - cost
            pname = o["product_name"]
            if pname not in result:
                result[pname] = {"revenue": 0, "cost": 0, "profit": 0}
            result[pname]["revenue"] += o["final_amount"]
            result[pname]["cost"] += cost
            result[pname]["profit"] += profit
    return result

def generate_insights(store_mode):
    orders = load_json("orders.json")
    mode_orders = [o for o in orders if o.get("store_mode") == store_mode]
    if not mode_orders:
        return ["No orders yet for this store mode."]

    insights = []
    total_rev = sum(o["final_amount"] for o in mode_orders)

    # Category insight
    cat_rev = get_category_revenue(store_mode)
    if cat_rev:
        top_cat = max(cat_rev, key=cat_rev.get)
        pct = round(cat_rev[top_cat] / total_rev * 100, 1)
        insights.append(f"📊 **{top_cat}** category generates **{pct}%** of total revenue")

    # Top products
    top_prods = get_top_products(store_mode, 3)
    if top_prods:
        top3_rev = sum(v for _, v in top_prods)
        top3_pct = round(top3_rev / total_rev * 100, 1)
        top_names = ", ".join(n for n, _ in top_prods[:2])
        insights.append(f"🏆 Top 3 products contribute **{top3_pct}%** of sales (led by {top_names})")

    # Stock alert
    products = load_json("products.json")
    low = [p["name"] for p in products if 0 < p["stock"] < 5]
    if low:
        insights.append(f"⚠️ **{len(low)} products** critically low on stock — reorder soon!")

    # Order volume
    insights.append(f"📦 Total of **{len(mode_orders)} orders** processed in this store mode")

    # Profit margin
    kpis = get_kpis(store_mode)
    insights.append(f"💰 Net profit margin is **{kpis['profit_margin']}%** — {'healthy' if kpis['profit_margin'] > 20 else 'needs attention'}")

    return insights
