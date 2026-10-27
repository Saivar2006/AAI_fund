# views/station_request_funds_view.py
import streamlit as st
from controllers.station_controller import StationController
from models.user_model import UserModel   # NEW IMPORT

PRIORITIES = ["Low", "Medium", "High"]

def station_request_funds_view():
    st.set_page_config(page_title="Request Funds", page_icon="💳", layout="wide")

    # Handle internal page routing
    if "go_to_page" in st.session_state:
        st.session_state["page"] = st.session_state["go_to_page"]
        del st.session_state["go_to_page"]
        st.rerun()

    if not st.session_state.get("logged_in"):
        st.error("Please login.")
        return

    # --------------------------
    # SIDEBAR NAVIGATION
    # --------------------------
    with st.sidebar:
        st.title("📌 Station Menu")
        st.button("🏠 Dashboard", on_click=lambda: go("station_dashboard"))
        st.button("📤 Update Usage", on_click=lambda: go("station_update_usage"))
        st.button("📜 History", on_click=lambda: go("station_history"))
        st.markdown("---")
        st.button("🚪 Logout", on_click=logout_action)

    st.markdown("## 💳 Request Funds")
    st.markdown("### Fill the details below")

    # --------------------------
    # FETCH ALL RHQ USERS
    # --------------------------
    rhq_users = UserModel.get_all_rhq_users()  # NEW FUNCTION WE WILL ADD
    if not rhq_users:
        st.error("No RHQ users available.")
        return

    # Convert to dropdown friendly format
    dropdown_labels = [
        f"{u['name']} — {u['email']}" for u in rhq_users
    ]
    id_mapping = {
        f"{u['name']} — {u['email']}": u["user_id"] for u in rhq_users
    }

    # --------------------------
    # FORM
    # --------------------------
    with st.form("req_form"):

        rhq_selected_label = st.selectbox("Send Request To (RHQ User)", dropdown_labels)
        rhq_user_id = id_mapping[rhq_selected_label]  # Extract correct ID

        amount = st.number_input("Amount (₹)", min_value=1.0, step=100.0)
        reason = st.text_area("Reason / Purpose")

        priority = st.selectbox("Priority", PRIORITIES, index=1)

        submitted = st.form_submit_button("Submit Request")

        if submitted:
            StationController.create_request(
                amount=amount,
                reason=reason,
                priority=priority,
                rhq_user_id=rhq_user_id  # NEW PARAM
            )

            st.success("Request submitted successfully!")
            st.balloons()


# --------------------------
# NAVIGATION HELPERS
# --------------------------
def go(page):
    st.session_state["go_to_page"] = page


def logout_action():
    from utils.session_manager import end_session
    end_session()
    st.session_state["go_to_page"] = "login"
