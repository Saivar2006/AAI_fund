# views/rhq_fund_pool_view.py
import streamlit as st
from controllers.rhq_fund_pool_controller import RHQFundPoolController
from utils.session_manager import end_session

def rhq_fund_pool_view():
    st.set_page_config(page_title="Fund Pool", page_icon="🏦", layout="wide")

    if not st.session_state.get("logged_in") or st.session_state.get("role") != "RHQ":
        st.error("Please login as RHQ user.")
        return

    pool = RHQFundPoolController.get_pool() or {"total_pool": 0}
    # Sidebar
    user_name = st.session_state.get("name") or "Unknown User"
    department = st.session_state.get("department") or "No Department"

    st.sidebar.markdown(f"### 👤 {user_name}")
    st.sidebar.markdown(f"**🏢 Department:** {department}")
    st.sidebar.markdown("---")

    if st.sidebar.button("🏠 Dashboard"):
        st.session_state["page"] = "rhq_dashboard"
        st.rerun()
    if st.sidebar.button("📤 Approve Requests"):
        st.session_state["page"] = "rhq_pending_requests"
        st.rerun()
    if st.sidebar.button("📜 Reports"):
        st.session_state["page"] = "rhq_reports"
        st.rerun()
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        end_session()
        st.session_state["page"] = "login"
        st.rerun()

    # Main
    st.markdown("## 🏦 Manage Fund Pool")
    st.markdown("Control the central RHQ fund pool used to approve station requests.")

    # Card style (same as station)
    st.markdown("""
        <style>
            .metric-card { background:#fff;border-radius:14px;padding:18px;box-shadow:0 4px 18px rgba(0,0,0,0.08);text-align:center; }
            .metric-value { font-size:28px;font-weight:700;color:#0b3d91; }
            .metric-label { font-size:14px;color:#666; }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Current Pool</div>"
                    f"<div class='metric-value'>₹ {float(pool.get('total_pool') or 0):.2f}</div></div>",
                    unsafe_allow_html=True)

    with col2:
        # simple stats placeholder: you can extend to show used_amount if needed
        used = pool.get("used_amount", 0) if pool else 0
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Used (record)</div>"
                    f"<div class='metric-value'>₹ {float(used or 0):.2f}</div></div>",
                    unsafe_allow_html=True)

    st.markdown("---")

    # Set pool
    with st.form("set_pool"):
        new_amount = st.number_input("Set pool amount (₹)", min_value=0.0, step=1000.0,
                                    value=float(pool.get("total_pool") or 0))
        submitted = st.form_submit_button("Set Pool")
        if submitted:
            RHQFundPoolController.set_pool(new_amount)
            st.success("Fund pool updated.")
            st.rerun()

    st.markdown("---")
    # Add to pool
    with st.form("add_pool"):
        add_amount = st.number_input("Add to pool (₹)", min_value=0.0, step=1000.0)
        add_sub = st.form_submit_button("Add Funds")
        if add_sub and add_amount > 0:
            RHQFundPoolController.add_pool(add_amount)
            st.success("Funds added to pool.")
            st.rerun()
