# views/rhq_reports_view.py
import streamlit as st
from controllers.rhq_reports_controller import RHQReportsController
from utils.session_manager import end_session

def rhq_reports_view():
    st.set_page_config(page_title="RHQ Reports", page_icon="📈", layout="wide")

    if not st.session_state.get("logged_in") or st.session_state.get("role") != "RHQ":
        st.error("Please login as RHQ user.")
        return

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
    if st.sidebar.button("🏦 Fund Pool"):
        st.session_state["page"] = "rhq_fund_pool"
        st.rerun()
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        end_session()
        st.session_state["page"] = "login"
        st.rerun()

    st.title("Reports")
    st.markdown("### Station-wise Fund Summary")
    sums = RHQReportsController.get_station_usage_summary()
    if sums:
        st.dataframe([
            {
                "Station": s["station_name"],
                "Assigned": f"₹ {float(s['assigned_amount']):.2f}",
                "Used": f"₹ {float(s['used_amount']):.2f}",
                "Residual": f"₹ {float(s['residual']):.2f}"
            } for s in sums
        ], use_container_width=True)
    else:
        st.info("No data yet.")

    st.markdown("---")
    st.markdown("### Recent Activity Logs")
    logs = RHQReportsController.get_activity_logs(100)
    if logs:
        for l in logs[:50]:
            who = l.get("user_name") or "System"
            station = l.get("station_name") or ""
            st.write(f"{l['created_at']} — {who} — {station} — {l['action_text']}")
    else:
        st.info("No activities yet.")
