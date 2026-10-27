# models/activity_model.py
from models.db import get_connection
import json

class ActivityModel:

    @staticmethod
    def log(user_id: int, station_id: int, action_text: str, meta: dict = None):
        conn = get_connection()
        cursor = conn.cursor()
        meta_json = json.dumps(meta) if meta else None
        query = "INSERT INTO activity_log (user_id, station_id, action_text, meta_json) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user_id, station_id, action_text, meta_json))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_recent(limit: int = 50):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT al.*, u.name as user_name, s.station_name FROM activity_log al LEFT JOIN users u ON al.user_id = u.user_id LEFT JOIN stations s ON al.station_id = s.station_id ORDER BY al.created_at DESC LIMIT %s"
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
