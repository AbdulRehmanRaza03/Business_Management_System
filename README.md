# 🛍️ SmartCommerce OS
### Multi-Region E-Commerce Store Management & Business Intelligence System

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com)

---

## 📌 Business Problem

Small and medium businesses struggle with:
- Tracking inventory across multiple channels
- Managing sales, orders, and customers manually
- Understanding profit/loss in real-time
- Handling national (PKR) vs international (USD) operations

**SmartCommerce OS solves all of this in one unified dashboard.**

---

## ✨ Features

| Module | Features |
|--------|---------|
| 🔐 Auth | Secure admin login |
| 🌍 Store Mode | National (PKR/17% GST) or International (USD/8% GST) |
| 📦 Products | Add, update, delete, search, stock tracking |
| 🧾 Orders | Create orders, auto tax/discount, invoice generation |
| 👤 Customers | CRM, purchase history, top customers ranking |
| 📊 Analytics | Power BI-style charts, trends, profit analysis |
| 📉 Inventory | Low stock alerts, overstock warnings, quick restock |
| 💰 P&L | Revenue, cost, net profit, margin breakdown |

---

## 🛠️ Tech Stack

- **Frontend/App**: Streamlit
- **Charts**: Plotly
- **Data**: JSON files (no database needed)
- **Language**: Python 3.9+

---

## 🚀 Run Locally

```bash
git clone https://github.com/yourname/smartcommerce-os
cd smartcommerce-os
pip install -r requirements.txt
streamlit run app.py
```

Login: `admin` / `admin123`

---

## ☁️ Deploy on Streamlit Cloud

1. Fork this repo to your GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path** to `app.py`
5. Click **Deploy**

---

## 📁 Project Structure

```
SmartCommerce-OS/
├── app.py              # Main entry + login + routing
├── requirements.txt
├── pages/
│   ├── dashboard.py    # KPI dashboard
│   ├── products.py     # Product management
│   ├── orders.py       # Order + invoice system
│   ├── customers.py    # Customer CRM
│   ├── analytics.py    # Business analytics
│   └── inventory.py    # Inventory alerts
├── utils/
│   ├── helpers.py      # File I/O, formatting, auth
│   └── calculations.py # KPIs, analytics computations
└── data/
    ├── products.json
    ├── orders.json
    ├── customers.json
    └── users.json
```

---

## 🔮 Future Improvements

- [ ] Multi-user roles (manager, staff)
- [ ] Export reports to PDF/Excel
- [ ] Email notifications for low stock
- [ ] Barcode scanner integration
- [ ] Multi-currency conversion API
- [ ] Supplier management module
- [ ] Mobile responsive PWA

---

*Built with ❤️ using Streamlit + Plotly*
