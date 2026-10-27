# controllers/rhq_reports_controller.py
from models.funds_model import FundsModel
from models.requests_model import RequestsModel
from models.activity_model import ActivityModel

class RHQReportsController:

    @staticmethod
    def get_station_usage_summary():
        # returns station funds (assigned/used/residual)
        return FundsModel.get_all_station_funds()

    @staticmethod
    def get_requests_summary():
        # return counts grouped by status (simple)
        rows = RequestsModel.get_all_requests_summary()  # we'll add this method below if needed
        return rows

    @staticmethod
    def get_activity_logs(limit=200):
        return ActivityModel.get_recent(limit)
