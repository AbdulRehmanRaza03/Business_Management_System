import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from utils.helpers import authenticate

st.set_page_config(
    page_title="SmartCommerce OS",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Sidebar */
[data-testid="stSidebar"] {background: linear-gradient(180deg,#0f1117 0%,#1a1d27 100%);}
[data-testid="stSidebar"] * {color:#e0e0e0 !important;}

/* KPI cards */
.kpi-card {
    background: linear-gradient(135deg,#1e2130,#252a3a);
    border:1px solid #2e3347;
    border-radius:12px;
    padding:20px 16px;
    text-align:center;
    margin-bottom:8px;
    box-shadow:0 4px 15px rgba(0,0,0,.3);
}
.kpi-value {font-size:1.8rem;font-weight:700;color:#7c83fd;}
.kpi-label {font-size:.8rem;color:#9ca3af;margin-top:4px;text-transform:uppercase;letter-spacing:.05em;}
.kpi-delta {font-size:.75rem;margin-top:4px;}

/* Alert boxes */
.alert-danger {background:#3b1f1f;border-left:4px solid #ef4444;padding:10px 14px;border-radius:6px;margin:6px 0;}
.alert-warning {background:#3b2f1a;border-left:4px solid #f59e0b;padding:10px 14px;border-radius:6px;margin:6px 0;}
.alert-success {background:#1a3b27;border-left:4px solid #10b981;padding:10px 14px;border-radius:6px;margin:6px 0;}
.alert-info {background:#1a2b3b;border-left:4px solid #3b82f6;padding:10px 14px;border-radius:6px;margin:6px 0;}

/* Section headers */
.section-header {
    background:linear-gradient(90deg,#7c83fd22,transparent);
    border-left:3px solid #7c83fd;
    padding:8px 14px;
    border-radius:0 8px 8px 0;
    margin:16px 0 12px 0;
    font-weight:600;
    font-size:1.05rem;
}

/* Badge */
.badge {display:inline-block;padding:2px 10px;border-radius:20px;font-size:.75rem;font-weight:600;}
.badge-blue {background:#1d4ed822;color:#60a5fa;border:1px solid #1d4ed844;}
.badge-green {background:#06652222;color:#34d399;border:1px solid #06652244;}
.badge-red {background:#7f1d1d22;color:#f87171;border:1px solid #7f1d1d44;}
.badge-yellow {background:#78350f22;color:#fbbf24;border:1px solid #78350f44;}

/* Login card */
.login-card {
    max-width:420px;
    margin:60px auto;
    background:linear-gradient(135deg,#1e2130,#252a3a);
    border:1px solid #2e3347;
    border-radius:16px;
    padding:40px 36px;
    box-shadow:0 8px 32px rgba(0,0,0,.4);
}

/* Table styling */
.styled-table {width:100%;border-collapse:collapse;}
.styled-table th {background:#1e2130;color:#9ca3af;font-size:.78rem;text-transform:uppercase;padding:10px 12px;border-bottom:1px solid #2e3347;}
.styled-table td {padding:10px 12px;border-bottom:1px solid #1e2130;font-size:.9rem;}
.styled-table tr:hover td {background:#1e213044;}

/* Divider */
.divider {border:none;border-top:1px solid #2e3347;margin:16px 0;}

/* Mode banner */
.mode-banner {
    background:linear-gradient(90deg,#7c83fd,#a78bfa);
    color:white;
    padding:8px 16px;
    border-radius:8px;
    font-weight:600;
    text-align:center;
    margin-bottom:16px;
}
</style>
""", unsafe_allow_html=True)


def login_page():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div class="login-card">
            <div style="text-align:center;margin-bottom:28px;">
                <div style="font-size:3rem;">🛍️</div>
                <h2 style="margin:8px 0 4px 0;color:#e0e0e0;">SmartCommerce OS</h2>
                <p style="color:#6b7280;font-size:.88rem;">Multi-Region E-Commerce Management</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🔐 Admin Login")
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")

        st.caption("Demo credentials: admin / admin123")

        if st.button("🚀 Login", use_container_width=True, type="primary"):
            if username and password:
                user = authenticate(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Try: admin / admin123")
            else:
                st.warning("Please enter both username and password.")


def store_mode_selection():
    st.markdown("""
    <div style="text-align:center;padding:20px 0 10px 0;">
        <div style="font-size:2.5rem;">🛍️</div>
        <h2 style="color:#e0e0e0;">Welcome, """ + st.session_state.user["name"] + """</h2>
        <p style="color:#9ca3af;">Select your store operating mode to continue</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("---")
        st.markdown("### 🌍 Choose Store Mode")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            <div class="kpi-card" style="cursor:pointer;">
                <div style="font-size:2.5rem;">🇵🇰</div>
                <div style="font-size:1.1rem;font-weight:600;color:#e0e0e0;margin-top:8px;">National Store</div>
                <div style="color:#9ca3af;font-size:.85rem;margin-top:6px;">PKR Currency • 17% GST • Local Market</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🇵🇰 Select National", use_container_width=True, type="primary"):
                st.session_state.store_mode = "national"
                st.rerun()

        with col_b:
            st.markdown("""
            <div class="kpi-card" style="cursor:pointer;">
                <div style="font-size:2.5rem;">🌍</div>
                <div style="font-size:1.1rem;font-weight:600;color:#e0e0e0;margin-top:8px;">International Store</div>
                <div style="color:#9ca3af;font-size:.85rem;margin-top:6px;">USD Currency • 8% GST • Global Market</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🌍 Select International", use_container_width=True):
                st.session_state.store_mode = "international"
                st.rerun()


def sidebar_nav():
    mode = st.session_state.get("store_mode", "national")
    flag = "🇵🇰" if mode == "national" else "🌍"
    currency = "PKR" if mode == "national" else "USD"

    with st.sidebar:
        st.markdown(f"""
        <div style="padding:16px 0 8px 0;text-align:center;">
            <div style="font-size:2rem;">🛍️</div>
            <div style="font-weight:700;font-size:1.1rem;color:#e0e0e0;">SmartCommerce OS</div>
            <div style="font-size:.78rem;color:#6b7280;">Business Intelligence System</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="mode-banner">{flag} {mode.title()} Mode · {currency}</div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Navigation**")

        pages = {
            "🏠 Dashboard": "dashboard",
            "📦 Products": "products",
            "🧾 Orders": "orders",
            "👤 Customers": "customers",
            "📊 Analytics": "analytics",
            "📉 Inventory Alerts": "inventory",
        }

        for label, key in pages.items():
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.current_page = key

        st.markdown("---")
        st.markdown(f"**Logged in as:** {st.session_state.user['name']}")
        if st.button("🔄 Switch Mode", use_container_width=True):
            del st.session_state["store_mode"]
            st.rerun()
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def main():
    # Init state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"

    if not st.session_state.logged_in:
        login_page()
        return

    if "store_mode" not in st.session_state:
        store_mode_selection()
        return

    sidebar_nav()

    page = st.session_state.get("current_page", "dashboard")

    if page == "dashboard":
        from pages.dashboard import show
        show()
    elif page == "products":
        from pages.products import show
        show()
    elif page == "orders":
        from pages.orders import show
        show()
    elif page == "customers":
        from pages.customers import show
        show()
    elif page == "analytics":
        from pages.analytics import show
        show()
    elif page == "inventory":
        from pages.inventory import show
        show()


if __name__ == "__main__":
    main()
