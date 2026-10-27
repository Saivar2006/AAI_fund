# controllers/rhq_controller.py
import streamlit as st
from models.fund_pool_model import FundPoolModel
from models.funds_model import FundsModel
from models.requests_model import RequestsModel
from models.activity_model import ActivityModel
from models.user_model import UserModel
from models.station_model import StationModel

class RHQController:

    @staticmethod
    def get_dashboard_data():
        user_id = st.session_state.get("user_id")
        if not user_id or st.session_state.get("role") != "RHQ":
            return {}

        # Fund pool
        pool = FundPoolModel.get_pool() or {"total_pool": 0}
        total_pool = float(pool.get("total_pool") or 0)

        # totals from funds table
        totals = FundsModel.get_totals() or {"total_assigned": 0, "total_used": 0}
        total_assigned = float(totals.get("total_assigned") or 0)
        total_used = float(totals.get("total_used") or 0)

        # pool remaining
        pool_remaining = total_pool - total_assigned
        if pool_remaining < 0:
            pool_remaining = 0

        # station-wise funds
        stations_funds = FundsModel.get_all_station_funds()

        # pending requests
        pending_requests = RequestsModel.get_pending_requests_for_rhq(user_id)

        # recent activity logs
        recent_activities = ActivityModel.get_recent(30)

        # station list
        all_stations = StationModel.get_all_stations()

        return {
            "user_id": user_id,
            "total_pool": total_pool,
            "total_assigned": total_assigned,
            "total_used": total_used,
            "pool_remaining": pool_remaining,   # <-- IMPORTANT FIX
            "stations_funds": stations_funds,
            "pending_requests": pending_requests,
            "recent_activities": recent_activities,
            "all_stations": all_stations
        }
