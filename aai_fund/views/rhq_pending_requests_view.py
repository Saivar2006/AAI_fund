# views/rhq_pending_requests_view.py
import streamlit as st
from controllers.rhq_controller import RHQController
from controllers.rhq_request_actions import RHQRequestActions
from utils.session_manager import end_session

def rhq_pending_requests_view():
    st.set_page_config(page_title="Pending Requests", page_icon="🔔", layout="wide")

    if not st.session_state.get("logged_in") or st.session_state.get("role") != "RHQ":
        st.error("Please login as RHQ user.")
        return

    data = RHQController.get_dashboard_data()
    pending = data.get("pending_requests", []) or []

    # Sidebar
    user_name = st.session_state.get("name") or "Unknown User"
    department = st.session_state.get("department") or "No Department"

    st.sidebar.markdown(f"### 👤 {user_name}")
    st.sidebar.markdown(f"**🏢 Department:** {department}")
    st.sidebar.markdown("---")

    if st.sidebar.button("🏠 Dashboard"):
        st.session_state["page"] = "rhq_dashboard"
        st.rerun()
    if st.sidebar.button("🏦 Fund Pool"):
        st.session_state["page"] = "rhq_fund_pool"
        st.rerun()
    if st.sidebar.button("📜 Reports"):
        st.session_state["page"] = "rhq_reports"
        st.rerun()
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        end_session()
        st.session_state["page"] = "login"
        st.rerun()

    st.title("Pending Requests Assigned To You")

    if not pending:
        st.info("No pending requests.")
        return

    # -----------------------------------------------------------
    #   FOR EACH PENDING REQUEST
    # -----------------------------------------------------------
    for r in pending:
        st.markdown("---")
        st.markdown(f"### 📝 Request #{r['request_id']} — Station: **{r['station_name']}**")

        st.markdown(f"**Amount:** ₹ {float(r['amount']):.2f}")
        st.markdown(f"**Priority:** {r['priority']}")
        st.markdown(f"**Requested by:** {r['requested_by']} ({r.get('requested_by_email','')})")
        st.markdown(f"**Reason:** {r.get('reason') or '-'}")

        # -------------------------------
        # COMMENT INPUT (MANDATORY)
        # -------------------------------
        comment = st.text_area(
            f"Enter comment for Request {r['request_id']} (Required)",
            key=f"comment_{r['request_id']}"
        )

        col1, col2, col3 = st.columns([1,1,4])

        # -------------------------------
        # APPROVE BUTTON
        # -------------------------------
        if col1.button(f"Approve {r['request_id']}", key=f"app_{r['request_id']}"):
            if not comment.strip():
                st.error("Comment is required to approve.")
            else:
                ok = RHQRequestActions.approve_request(r['request_id'], comment)
                if ok:
                    st.success(f"Request {r['request_id']} approved with comment.")
                    st.rerun()
                else:
                    st.error("Something went wrong while approving.")

        # -------------------------------
        # REJECT BUTTON
        # -------------------------------
        if col2.button(f"Reject {r['request_id']}", key=f"rej_{r['request_id']}"):
            if not comment.strip():
                st.error("Comment is required to reject.")
            else:
                ok = RHQRequestActions.reject_request(r['request_id'], comment)
                if ok:
                    st.success(f"Request {r['request_id']} rejected with comment.")
                    st.rerun()
                else:
                    st.error("Something went wrong while rejecting.")


