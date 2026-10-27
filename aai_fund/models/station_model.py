# models/station_model.py
from models.db import get_connection

class StationModel:

    @staticmethod
    def get_all_stations():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT station_id, station_name FROM stations ORDER BY station_name")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def upsert_station(station_id: int, station_name: str):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO stations (station_id, station_name)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE station_name = VALUES(station_name)
        """
        cursor.execute(query, (station_id, station_name))
        conn.commit()
        cursor.close()
        conn.close()
