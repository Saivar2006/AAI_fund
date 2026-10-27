# views/station_update_usage_view.py
import streamlit as st
from controllers.station_controller import StationController

def station_update_usage_view():
    st.set_page_config(page_title="Update Usage", page_icon="🧾", layout="wide")

    if "go_to_page" in st.session_state:
        st.session_state["page"] = st.session_state["go_to_page"]
        del st.session_state["go_to_page"]
        st.rerun()

    if not st.session_state.get("logged_in"):
        st.error("Please login.")
        return

    with st.sidebar:
        st.title("📌 Station Menu")
        st.button("🏠 Dashboard", on_click=lambda: go("station_dashboard"))
        st.button("💳 Request Funds", on_click=lambda: go("station_request_funds"))
        st.button("📜 History", on_click=lambda: go("station_history"))
        st.markdown("---")
        st.button("🚪 Logout", on_click=logout_action)

    st.markdown("## 🧾 Update Fund Usage")
    st.markdown("### Add Usage Details")

    with st.form("usage_form"):
        amount = st.number_input("Amount Used (₹)", min_value=1.0, step=50.0)
        purpose = st.text_area("Purpose / Description")
        uploaded_file = st.file_uploader("Upload Receipt (optional)",
                                         type=["pdf", "png", "jpg", "jpeg"])

        submitted = st.form_submit_button("Submit Usage")
        if submitted:
            file_meta = None
            if uploaded_file:
                file_meta = {"filename": uploaded_file.name, "type": uploaded_file.type}
            StationController.update_usage(amount, purpose, file_meta)
            st.success("Usage updated!")
            st.balloons()

def go(page):
    st.session_state["go_to_page"] = page

def logout_action():
    from utils.session_manager import end_session
    end_session()
    st.session_state["go_to_page"] = "login"
