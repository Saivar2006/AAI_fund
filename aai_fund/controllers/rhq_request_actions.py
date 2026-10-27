# controllers/rhq_request_actions.py
import streamlit as st
from models.requests_model import RequestsModel
from models.fund_pool_model import FundPoolModel
from models.funds_model import FundsModel
from models.activity_model import ActivityModel

class RHQRequestActions:

    # ===============================================================
    # APPROVE REQUEST WITH COMMENT
    # ===============================================================
    @staticmethod
    def approve_request(request_id: int, comment: str):
        rhq_user_id = st.session_state.get("user_id")

        if not rhq_user_id or st.session_state.get("role") != "RHQ":
            st.error("Only RHQ users can approve requests.")
            return False

        # Fetch request
        req = RequestsModel.get_request_by_id(request_id)
        if not req:
            st.error("Request not found.")
            return False

        station_id = req["station_id"]
        amount = float(req["amount"])

        # Check RHQ pool
        ok = FundPoolModel.deduct_from_pool(amount)
        if not ok:
            st.error("Insufficient RHQ pool funds.")
            return False

        # Assign funds to station
        FundsModel.assign_funds(station_id, amount)

        # Update status + save comment + save who approved
        RequestsModel.update_request_status(
            request_id=request_id,
            status="Approved",
            approved_by=rhq_user_id,   # ✅ CORRECT argument
            comment=comment
        )

        # Log activity
        ActivityModel.log(
            rhq_user_id,
            station_id,
            f"Approved request #{request_id} for ₹{amount:.2f}",
            {"request_id": request_id, "comment": comment}
        )

        return True

    # ===============================================================
    # REJECT REQUEST WITH COMMENT
    # ===============================================================
    @staticmethod
    def reject_request(request_id: int, comment: str):
        rhq_user_id = st.session_state.get("user_id")

        if not rhq_user_id or st.session_state.get("role") != "RHQ":
            st.error("Only RHQ users can reject requests.")
            return False

        # Update status + comment + who rejected
        RequestsModel.update_request_status(
            request_id=request_id,
            status="Rejected",
            approved_by=rhq_user_id,  # ✅ CORRECT argument
            comment=comment
        )

        # Activity log
        ActivityModel.log(
            rhq_user_id,
            None,
            f"Rejected request #{request_id}",
            {"request_id": request_id, "comment": comment}
        )

        return True


