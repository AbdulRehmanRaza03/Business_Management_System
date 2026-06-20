<p align="center">
  <img src="https://img.shields.io/badge/SmartCommerce%20OS-v1.0.0-7c83fd?style=for-the-badge&logo=shopify&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Plotly-5.17+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge" />
</p>

<h1 align="center">🛍️ SmartCommerce OS</h1>
<h3 align="center">Multi-Region E-Commerce Store Management & Business Intelligence System</h3>

<p align="center">
  <i>A production-grade SaaS dashboard built with Python & Streamlit — designed to solve real-world inventory, sales, and profit tracking challenges for small & medium businesses.</i>
</p>

<p align="center">
  <a href="https://abdulrehmanraza03.github.io/My-Portfolio/"><strong>🌐 Portfolio</strong></a> &nbsp;·&nbsp;
  <a href="https://github.com/AbdulRehmanRaza03"><strong>💻 GitHub</strong></a> &nbsp;·&nbsp;
  <a href="https://www.linkedin.com/in/abdul-rehman-raza-7a125b332"><strong>🔗 LinkedIn</strong></a>
</p>

---

## 📌 Table of Contents

- [The Problem](#-the-problem)
- [Solution Overview](#-solution-overview)
- [System Architecture](#️-system-architecture)
- [Modules Deep Dive](#-modules-deep-dive)
- [How It Works](#-how-it-works-flow)
- [Tech Stack](#️-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Run](#-installation--run)
- [Deploy on Streamlit Cloud](#️-deploy-on-streamlit-cloud)
- [My Other Projects](#-my-other-projects)
- [Connect With Me](#-connect-with-me)
- [Future Roadmap](#-future-roadmap)

---

## ❓ The Problem

Small and medium businesses in Pakistan and globally face these daily struggles:

| Problem | Impact |
|---------|--------|
| 📦 No real-time inventory tracking | Stock-outs → Lost sales |
| 🧾 Manual order processing | Errors, delays, no audit trail |
| 💸 No profit/loss visibility | Decisions made blind |
| 🌍 Managing national vs international sales | Currency confusion, wrong tax |
| 👤 No customer history | Can't identify top buyers or retention |
| 📊 No business intelligence | Can't spot trends or top products |

**SmartCommerce OS is a one-dashboard solution that eliminates all of these.**

---

## ✅ Solution Overview

SmartCommerce OS is a **fully functional, multi-module business management system** that mimics the functionality of enterprise tools like Shopify Admin, Zoho Inventory, and Power BI — built entirely in Python with zero paid services.

```
One login → Choose store mode → Manage everything from a single dashboard
```

Key differentiators:
- 🇵🇰 **National mode** — PKR currency, 17% GST (Pakistan tax law)
- 🌍 **International mode** — USD currency, 8% GST (global standard)
- 🔄 **Switch modes live** without losing data
- 📊 **Auto-generated business insights** from your own data
- 🚨 **Real-time inventory alerts** with one-click restock

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     SmartCommerce OS                        │
├─────────────────────────────────────────────────────────────┤
│                        app.py                               │
│          Login → Store Mode → Sidebar → Page Router         │
├──────────┬──────────┬──────────┬──────────┬────────────────┤
│Dashboard │ Products │  Orders  │Customers │Analytics/Alerts│
│  Page    │   Page   │   Page   │   Page   │    Pages       │
├──────────┴──────────┴──────────┴──────────┴────────────────┤
│                    Utils Layer                              │
│         helpers.py           calculations.py               │
│   (I/O, auth, formatting)  (KPIs, charts data, insights)   │
├─────────────────────────────────────────────────────────────┤
│                    Data Layer (JSON)                        │
│  products.json  orders.json  customers.json  users.json     │
└─────────────────────────────────────────────────────────────┘
```

**Data flows one-way:** UI → Utils → JSON files → Utils → UI

No database required. All data stored in structured JSON files — making it fully portable and deployable on any platform.

---

## 🧩 Modules Deep Dive

### 🔐 Module 1 — Authentication System
- File-based login using `users.json`
- Session state management via `st.session_state`
- Logout + mode-switching without full page reload
- Extensible to multi-role (admin / staff) in future

### 🌍 Module 2 — Store Mode Engine
This is the core innovation. On startup, user selects:

| Setting | 🇵🇰 National | 🌍 International |
|---------|------------|----------------|
| Currency | PKR | USD |
| Tax Rate | 17% GST | 8% GST |
| Tax Label | "GST (17%)" | "GST (8%)" |
| Price Format | `PKR 1,10,000` | `$299.99` |

All calculations, displays, and exports automatically adjust.

### 📦 Module 3 — Product Management
- Auto-generated Product IDs (`PRD + 6 digits`)
- Full CRUD: Add, Update, Delete, Search
- Filters by category, stock status, sort order
- Live margin % calculator per product
- Stock tracking integrated with order deduction

### 🧾 Module 4 — Order Management & Invoicing
Order flow:
```
Select Customer → Select Product → Set Qty → Apply Discount
→ Auto-calculate Tax → Preview Total → Confirm → Invoice Generated
```
- Inventory auto-decrements on order creation
- Customer spending totals auto-update
- Full order history with all financial fields
- Invoice card displayed post-confirmation

### 👤 Module 5 — Customer CRM
- Customer profiles: name, phone, email, city
- Full purchase history per customer per store mode
- Top customers ranked by spending with bar chart
- Medal rankings (🥇🥈🥉) for top 3 spenders
- Customer-level KPIs: total orders, total spent

### 📊 Module 6 — Business Analytics (Power BI Style)
7 interactive Plotly charts:
1. **Monthly Revenue Trend** — area line chart with data labels
2. **Top Products** — horizontal bar chart ranked by revenue
3. **Category Revenue** — donut pie chart
4. **Stock Distribution** — bar chart by category
5. **P&L Breakdown** — grouped bars (Revenue vs Cost vs Profit)
6. **Profit per Product** — cost vs revenue vs profit per item
7. **National vs International Comparison** — side-by-side bar chart

Auto-generated text insights like:
> 📊 Electronics category generates **85.4%** of total revenue
> 🏆 Top 3 products contribute **60.5%** of sales

### 📉 Module 7 — Inventory Alert System
- Configurable low-stock and overstock thresholds (via sliders)
- Color-coded alert levels:
  - 🔴 Out of Stock → immediate action
  - 🟡 Low Stock → reorder warning
  - 🟢 Healthy → all good
  - 🔵 Overstock → promotion suggested
- Horizontal reference lines on stock chart
- One-click Quick Restock form

### 💰 Module 8 — Profit & Loss Engine
Calculation logic:
```python
subtotal    = unit_price × quantity
discounted  = subtotal - discount
tax_amount  = discounted × tax_rate   # 17% or 8%
final       = discounted + tax_amount

profit      = final_amount - (purchase_price × quantity)
margin %    = (profit / revenue) × 100
```

---

## 🔄 How It Works (Flow)

```
User visits app
       │
       ▼
  Login Screen  ──── Wrong creds ──→ Error
       │ ✅ Correct
       ▼
 Store Mode Selection
  🇵🇰 National  or  🌍 International
       │
       ▼
  Sidebar Navigation
  ┌────────────────────┐
  │ 🏠 Dashboard       │ ← KPIs + charts + recent orders
  │ 📦 Products        │ ← Inventory CRUD
  │ 🧾 Orders          │ ← New order + invoice
  │ 👤 Customers       │ ← CRM + history
  │ 📊 Analytics       │ ← BI charts
  │ 📉 Inventory Alerts│ ← Stock monitoring
  └────────────────────┘
       │
       ▼
  All pages read/write JSON data
  All calculations adjust to selected store mode
```

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.9+ | Core language |
| Streamlit | 1.28+ | Web UI framework |
| Plotly | 5.17+ | Interactive charts |
| Pandas | 2.0+ | Data manipulation |
| JSON | built-in | File-based database |
| datetime | built-in | Timestamps & ordering |
| os / random | built-in | File paths & ID generation |

**Zero paid APIs. Zero external databases. Fully offline-capable.**

---

## 📁 Project Structure

```
SmartCommerce-OS/
│
├── app.py                  # 🚀 Entry point: login, mode select, routing
│
├── pages/
│   ├── __init__.py
│   ├── dashboard.py        # 📊 KPI cards + 4 live charts + recent orders
│   ├── products.py         # 📦 Full product CRUD + search + filters
│   ├── orders.py           # 🧾 Order creation + invoice + history
│   ├── customers.py        # 👤 CRM + purchase history + top customers
│   ├── analytics.py        # 📈 7 Plotly charts + P&L + comparison
│   └── inventory.py        # 📉 Alerts + stock chart + quick restock
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py          # 🔧 JSON I/O, auth, formatting, tax logic
│   └── calculations.py     # 🧮 KPIs, insights engine, profit analysis
│
├── data/
│   ├── products.json       # 10 seeded products
│   ├── orders.json         # 10 seeded orders
│   ├── customers.json      # 5 seeded customers
│   └── users.json          # Admin credentials
│
├── requirements.txt
└── README.md
```

---

## 🚀 Installation & Run

### Prerequisites
- Python 3.9 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/AbdulRehmanRaza03/SmartCommerce-OS
cd SmartCommerce-OS

# 2. (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

App opens at: `http://localhost:8501`

**Login credentials:**
```
Username: admin
Password: admin123
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push this project to your GitHub repository
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"**
4. Select your repository & branch
5. Set **Main file path** → `app.py`
6. Click **Deploy** 🚀

Your app will be live at: `https://your-app-name.streamlit.app`

> ⚡ Free hosting, no credit card required.

---

## 🌐 My Other Projects

| Project | Description | Live Demo |
|---------|-------------|-----------|
| 🛍️ **ABD Wears** | E-Commerce fashion website | [Visit →](https://abdulrehmanraza03.github.io/ABD-Wears-Weabsite/#/) |
| 🍕 **FFC Pizza** | Restaurant ordering website | [Visit →](https://abdulrehmanraza03.github.io/FFC_Pizza_Restaurent/) |
| 🌐 **Web Service App** | Multi-tool web service platform | [Visit →](https://replit-tool--theabdulservice.replit.app/#collections) |
| 🎥 **Screen Recorder** | Browser-based screen recording web app | [Visit →](https://abd-screen-recorder-web-app.streamlit.app/) |
| 📉 **Customer Churn Prediction** | ML-powered data science dashboard | [Visit →](https://customer-churn-prediction-analytics-5syak8uuar5rp4f8ihphvs.streamlit.app/) |

---

## 👨‍💻 Connect With Me

<p align="center">

| Platform | Link |
|----------|------|
| 🌐 Portfolio | [abdulrehmanraza03.github.io/My-Portfolio](https://abdulrehmanraza03.github.io/My-Portfolio/) |
| 💻 GitHub | [github.com/AbdulRehmanRaza03](https://github.com/AbdulRehmanRaza03) |
| 🔗 LinkedIn | [linkedin.com/in/abdul-rehman-raza-7a125b332](https://www.linkedin.com/in/abdul-rehman-raza-7a125b332) |
| 📧 Email | [abdulrehmanraza60@gmail.com](mailto:abdulrehmanraza60@gmail.com) |
| 📱 Phone | +92 318 1678758 |

</p>

---

## 🔮 Future Roadmap

- [ ] 👥 Multi-user roles (Admin, Manager, Sales Staff)
- [ ] 📄 Export invoices to PDF
- [ ] 📊 Export reports to Excel (.xlsx)
- [ ] 📧 Email alerts for low stock via SMTP
- [ ] 🔢 Barcode scanner integration
- [ ] 💱 Live currency conversion via API
- [ ] 📦 Supplier management module
- [ ] 📱 Mobile-responsive PWA version
- [ ] 🗄️ SQLite/PostgreSQL database upgrade
- [ ] 🌙 Dark/Light theme toggle

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

<p align="center">
  <b>Built with ❤️ by Abdul Rehman Raza</b><br>
  <a href="https://abdulrehmanraza03.github.io/My-Portfolio/">Portfolio</a> · 
  <a href="https://github.com/AbdulRehmanRaza03">GitHub</a> · 
  <a href="https://www.linkedin.com/in/abdul-rehman-raza-7a125b332">LinkedIn</a>
</p>
