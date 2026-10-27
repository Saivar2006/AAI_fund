# controllers/station_controller.py
import streamlit as st
from models.funds_model import FundsModel
from models.requests_model import RequestsModel
from models.activity_model import ActivityModel
from models.usage_updates_model import UsageUpdatesModel  # NEW

class StationController:

    @staticmethod
    def get_dashboard_data():
        user_id = st.session_state.get("user_id")
        station_id = st.session_state.get("station_id")
        station_name = st.session_state.get("station_name")

        fund = FundsModel.get_fund_by_station(station_id) or {"assigned_amount": 0, "used_amount": 0}

        assigned = float(fund.get("assigned_amount") or 0)
        used = float(fund.get("used_amount") or 0)
        residual = assigned - used

        pending_requests = RequestsModel.get_requests_by_station(station_id)

        try:
            recent_activities = ActivityModel.get_recent(20)
        except Exception:
            recent_activities = []

        return {
            "user_id": user_id,
            "station_id": station_id,
            "station_name": station_name,
            "assigned": assigned,
            "used": used,
            "residual": residual,
            "pending_requests": pending_requests,
            "recent_activities": recent_activities
        }

    @staticmethod
    def create_request(amount: float, reason: str, priority: str, rhq_user_id: int):
        user_id = st.session_state.get("user_id")
        station_id = st.session_state.get("station_id")

        if not user_id or not station_id:
            st.error("Invalid session. Please login again.")
            return

        # Validate amount
        try:
            amt = float(amount)
            if amt <= 0:
                st.error("Amount must be greater than 0.")
                return
        except Exception:
            st.error("Invalid amount format.")
            return

        # Insert request with RHQ receiver
        req_id = RequestsModel.create_request(
            user_id=user_id,
            station_id=station_id,
            amount=amt,
            reason=reason,
            priority=priority,
            rhq_user_id=rhq_user_id
        )

        # Log activity
        activity_text = f"Requested ₹{amt:.2f} ({priority}) — {reason}"
        ActivityModel.log(
            user_id,
            station_id,
            activity_text,
            {"request_id": req_id, "amount": amt, "priority": priority, "sent_to_rhq": rhq_user_id}
        )

        st.success("Request submitted successfully!")
        st.session_state["page"] = "station_dashboard"
        st.rerun()

    @staticmethod
    def update_usage(amount: float, purpose: str, file_meta: dict = None):
        user_id = st.session_state.get("user_id")
        station_id = st.session_state.get("station_id")

        if not user_id or not station_id:
            st.error("Invalid session. Please login again.")
            return

        try:
            amt = float(amount)
            if amt <= 0:
                st.error("Amount must be greater than 0.")
                return
        except Exception:
            st.error("Invalid amount format.")
            return

        # Update fund usage
        FundsModel.update_used_amount(station_id, amt)

        # Log activity
        meta = {"purpose": purpose}
        if file_meta:
            meta["file"] = file_meta
        action_text = f"Updated usage ₹{amt:.2f} — {purpose}"
        ActivityModel.log(user_id, station_id, action_text, meta)

        # **Insert usage record into usage_updates table**
        UsageUpdatesModel.create_usage(station_id, amt, purpose)

        st.success("Usage updated!")
        st.session_state["page"] = "station_dashboard"
        st.rerun()
