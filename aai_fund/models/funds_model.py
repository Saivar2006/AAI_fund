#models/funds_model.py
from models.db import get_connection
from decimal import Decimal

class FundsModel:

    # ----------------------------------------------------
    # GET FUND FOR ONE STATION
    # ----------------------------------------------------
    @staticmethod
    def get_fund_by_station(station_id: int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM funds WHERE station_id = %s LIMIT 1"
        cursor.execute(query, (station_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    # ----------------------------------------------------
    # CREATE FUND ROW IF STATION IS NEW
    # ----------------------------------------------------
    @staticmethod
    def create_fund_for_station(station_id: int, assigned_amount: float = 0.0):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO funds (station_id, assigned_amount, used_amount)
            VALUES (%s, %s, 0)
            ON DUPLICATE KEY UPDATE
                assigned_amount = assigned_amount + VALUES(assigned_amount)
        """
        cursor.execute(query, (station_id, assigned_amount))
        conn.commit()
        cursor.close()
        conn.close()

    # ----------------------------------------------------
    # STATION — UPDATE USED AMOUNT
    # ----------------------------------------------------
    @staticmethod
    def update_used_amount(station_id: int, used_delta: float):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE funds 
            SET used_amount = used_amount + %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE station_id = %s
        """
        cursor.execute(query, (used_delta, station_id))
        conn.commit()
        cursor.close()
        conn.close()

    # ----------------------------------------------------
    # RHQ — ADD FUNDS TO STATION
    # (for manual allocation, not request approval)
    # ----------------------------------------------------
    @staticmethod
    def assign_funds(station_id: int, amount: float):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO funds (station_id, assigned_amount, used_amount)
            VALUES (%s, %s, 0)
            ON DUPLICATE KEY UPDATE 
                assigned_amount = assigned_amount + %s,
                updated_at = CURRENT_TIMESTAMP
        """
        cursor.execute(query, (station_id, amount, amount))
        conn.commit()
        cursor.close()
        conn.close()

    # ----------------------------------------------------
    # RHQ — SET EXPLICIT ASSIGNED AMOUNT
    # (used in RHQ → Manage Stations)
    # ----------------------------------------------------
    @staticmethod
    def set_assigned_amount(station_id: int, new_amount: float):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO funds (station_id, assigned_amount, used_amount)
            VALUES (%s, %s, 0)
            ON DUPLICATE KEY UPDATE 
                assigned_amount = %s,
                updated_at = CURRENT_TIMESTAMP
        """
        cursor.execute(query, (station_id, new_amount, new_amount))
        conn.commit()
        cursor.close()
        conn.close()

    # ----------------------------------------------------
    # RHQ — GET ALL STATIONS & FUND STATUS
    # ----------------------------------------------------
    @staticmethod
    def get_all_station_funds():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT s.station_id, s.station_name,
                   IFNULL(f.assigned_amount,0) AS assigned_amount,
                   IFNULL(f.used_amount,0) AS used_amount,
                   (IFNULL(f.assigned_amount,0) - IFNULL(f.used_amount,0)) AS residual
            FROM stations s
            LEFT JOIN funds f ON s.station_id = f.station_id
            ORDER BY s.station_name
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    # ----------------------------------------------------
    # SUMMARY TOTALS (used in RHQ Dashboard)
    # ----------------------------------------------------
    @staticmethod
    def get_totals():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                SUM(IFNULL(assigned_amount,0)) AS total_assigned,
                SUM(IFNULL(used_amount,0)) AS total_used
            FROM funds
        """
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row or {"total_assigned": 0, "total_used": 0}

    # ----------------------------------------------------
    # RHQ — GET RESIDUAL FOR A STATION
    # ----------------------------------------------------
    @staticmethod
    def get_station_residual(station_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT (assigned_amount - used_amount)
            FROM funds WHERE station_id = %s
        """
        cursor.execute(query, (station_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return float(row[0]) if row else 0.0

    # ----------------------------------------------------
    # RHQ — DEDUCT FROM FUND POOL ON APPROVAL
    # (This will work with fund_pool_model)
    # ----------------------------------------------------
    @staticmethod
    def add_to_station_from_rhq(station_id: int, amount: float):
        """Used only when RHQ approves a request."""
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE funds
            SET assigned_amount = assigned_amount + %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE station_id = %s
        """
        cursor.execute(query, (amount, station_id))
        conn.commit()
        cursor.close()
        conn.close()
