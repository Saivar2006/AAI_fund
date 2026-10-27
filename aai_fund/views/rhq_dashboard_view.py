# views/rhq_dashboard_view.py
import streamlit as st
from controllers.rhq_controller import RHQController
from utils.session_manager import end_session

def rhq_dashboard_view():
    st.set_page_config(page_title="RHQ Dashboard", page_icon="🏢", layout="wide")

    # ---- Authentication Check ----
    if not st.session_state.get("logged_in"):
        st.error("Please login.")
        if st.button("Go to Login"):
            st.session_state["page"] = "login"
            st.rerun()
        return

    # ---- Load RHQ Data ----
    data = RHQController.get_dashboard_data()

    # ---- SIDEBAR ----
    user_name = st.session_state.get("name") or "Unknown User"
    department = st.session_state.get("department") or "No Department"

    st.sidebar.markdown(f"### 👤 {user_name}")
    st.sidebar.markdown(f"**🏢 Department:** {department}")
    st.sidebar.markdown("---")

    if st.sidebar.button("🏠 Dashboard"):
        st.session_state["page"] = "rhq_dashboard"
        st.rerun()

    if st.sidebar.button("➕ Add Funds to Pool"):
        st.session_state["page"] = "rhq_fund_pool"
        st.rerun()

    if st.sidebar.button("📤 Approve Requests"):
        st.session_state["page"] = "rhq_pending_requests"
        st.rerun()

    if st.sidebar.button("📜 View All Requests"):
        st.session_state["page"] = "rhq_reports"   # FIXED
        st.rerun()

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        end_session()
        st.session_state["page"] = "login"
        st.rerun()

        
    # =================================================================
    #                        MAIN DASHBOARD
    # =================================================================

    st.markdown("## 🏢 RHQ Dashboard")
    st.markdown("### Fund Pool Overview & Station Status")

    # ===== METRIC CARDS =====
    card_style = """
        <style>
            .metric-card {
                background: #ffffff;
                border-radius: 14px;
                padding: 22px;
                box-shadow: 0 4px 18px rgba(0,0,0,0.08);
                text-align: center;
            }
            .metric-value {
                font-size: 28px;
                font-weight: bold;
                color: #0b3d91;
            }
            .metric-label {
                font-size: 16px;
                color: #666;
            }
        </style>
    """
    st.markdown(card_style, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"<div class='metric-card'><div class='metric-label'>Total Fund Pool</div>"
            f"<div class='metric-value'>₹ {data['total_pool']:.2f}</div></div>",
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"<div class='metric-card'><div class='metric-label'>Total Assigned to Stations</div>"
            f"<div class='metric-value'>₹ {data['total_assigned']:.2f}</div></div>",
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"<div class='metric-card'><div class='metric-label'>Pool Remaining</div>"
            f"<div class='metric-value'>₹ {data['pool_remaining']:.2f}</div></div>",
            unsafe_allow_html=True
        )

    # ===============================================================
    #                   BODY SECTION
    # ===============================================================

    col_left, col_right = st.columns([1.7, 1.3])

    # ---- Pending Requests ----
    with col_left:
        st.markdown("### 📌 Pending Fund Requests")

        pending = data["pending_requests"] or []

        if not pending:
            st.info("No pending requests.")
        else:
            st.dataframe(
                [
                    {
                        "Request ID": r["request_id"],
                        "Station": r["station_name"],
                        "Amount": f"₹ {float(r['amount']):.2f}",
                        "Priority": r["priority"],
                        "Status": r["status"],
                        "Created": r["created_at"]
                    }
                    for r in pending
                ],
                use_container_width=True
            )

    # ---- Recent Activity ----
    with col_right:
        st.markdown("### 🕒 Recent Activity")

        acts = data["recent_activities"] or []
        if not acts:
            st.info("No recent activity.")
        else:
            for a in acts[:8]:
                who = a.get("user_name", "System")
                station = a.get("station_name", "")
                st.markdown(
                    f"""
                    <div style='margin-bottom:10px;
                                padding:10px;
                                background:#f7f9fc;
                                border-radius:10px;
                                border-left: 4px solid #0b3d91;'>
                        <b>{a['created_at']}</b><br>
                        {who} • {station}<br>
                        <span style='color:#444;'>{a['action_text']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
