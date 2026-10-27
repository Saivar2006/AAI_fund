# models/usage_updates_model.py
from models.db import get_connection

class UsageUpdatesModel:
    @staticmethod
    def create_usage(station_id: int, amount_used: float, description: str):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO usage_updates (station_id, amount_used, description)
            VALUES (%s, %s, %s)
        """, (station_id, amount_used, description))
        conn.commit()
        cursor.close()
        conn.close()
