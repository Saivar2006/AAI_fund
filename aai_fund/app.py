# app.py
import streamlit as st

# --- AUTH + REGISTRATION ---
from views.login_view import login_view
from views.choose_role_view import choose_role_view
from views.register_rhq_view import register_rhq_view
from views.register_station_view import register_station_view

# --- STATION VIEWS ---
from views.station_dashboard_view import station_dashboard_view
from views.station_request_funds_view import station_request_funds_view
from views.station_update_usage_view import station_update_usage_view

def main():
    # Default page
    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    page = st.session_state["page"]

    # -------------------------------
    # AUTH FLOW
    # -------------------------------
    if page == "login":
        login_view()

    elif page == "choose_role":
        choose_role_view()

    elif page == "register_rhq":
        register_rhq_view()

    elif page == "register_station":
        register_station_view()

    # -------------------------------
    # STATION FLOW 
    # -------------------------------
    elif page == "station_dashboard":
        station_dashboard_view()

    elif page == "station_request_funds":
        station_request_funds_view()

    elif page == "station_update_usage":
        station_update_usage_view()

    # -------------------------------
    # RHQ FLOW 
    # -------------------------------
    elif page == "rhq_dashboard":
        from views.rhq_dashboard_view import rhq_dashboard_view
        rhq_dashboard_view()

    elif page == "rhq_pending_requests":
        from views.rhq_pending_requests_view import rhq_pending_requests_view
        rhq_pending_requests_view()

    elif page == "rhq_fund_pool":
        from views.rhq_fund_pool_view import rhq_fund_pool_view
        rhq_fund_pool_view()

    elif page == "rhq_reports":   # FIXED
        from views.rhq_reports_view import rhq_reports_view
        rhq_reports_view()

if __name__ == "__main__":
    main()
