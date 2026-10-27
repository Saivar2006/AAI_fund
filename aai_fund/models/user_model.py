# models/user_model.py
from models.db import get_connection

class UserModel:

    @staticmethod
    def get_user_by_email(email: str):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT user_id, name, designation, email, password_hash, role, department, station_id, station_name
            FROM users
            WHERE email = %s
            LIMIT 1
        """
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def create_user(
        name: str,
        designation: str,
        email: str,
        password_hash: str,
        role: str,
        department: str,
        station_id: int = None,
        station_name: str = None
    ):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO users (name, designation, email, password_hash, role, department, station_id, station_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, designation, email, password_hash, role, department, station_id, station_name))
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return user_id

    @staticmethod
    def get_all_rhq_users():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT user_id, name, email
            FROM users
            WHERE role = 'rhq'
            ORDER BY name ASC
        """
        cursor.execute(query)
        rhq_users = cursor.fetchall()
        cursor.close()
        conn.close()
        return rhq_users
