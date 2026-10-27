# controllers/rhq_fund_pool_controller.py
import streamlit as st
from models.fund_pool_model import FundPoolModel
from models.activity_model import ActivityModel

class RHQFundPoolController:

    @staticmethod
    def get_pool():
        return FundPoolModel.get_pool()

    @staticmethod
    def set_pool(amount: float):
        user_id = st.session_state.get("user_id")
        FundPoolModel.create_or_set_pool(amount)
        ActivityModel.log(user_id, None, f"Set fund pool to ₹{amount:.2f}", {"pool_set": amount})

    @staticmethod
    def add_pool(amount: float):
        user_id = st.session_state.get("user_id")
        FundPoolModel.add_to_pool(amount)
        ActivityModel.log(user_id, None, f"Added ₹{amount:.2f} to fund pool", {"add": amount})
