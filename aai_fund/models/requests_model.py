from models.db import get_connection

class RequestsModel:

    # ------------------------------------------------------
    # CREATE NEW REQUEST — station → specific RHQ user
    # ------------------------------------------------------
    @staticmethod
    def create_request(user_id: int, station_id: int, rhq_user_id: int,
                       amount: float, reason: str, priority: str):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO requests
            (user_id, station_id, rhq_user_id, amount, reason, priority)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (user_id, station_id, rhq_user_id,
                               amount, reason, priority))
        conn.commit()

        req_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return req_id

    # ------------------------------------------------------
    # RHQ — GET ALL REQUESTS SENT TO ME
    # ------------------------------------------------------
    @staticmethod
    def get_pending_requests_for_rhq(rhq_user_id: int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                r.*,
                u.name AS requested_by,
                u.email AS requested_by_email,
                s.station_name,
                rhq.name AS rhq_receiver,
                rhq.email AS rhq_receiver_email
            FROM requests r
            JOIN users u ON r.user_id = u.user_id
            JOIN stations s ON r.station_id = s.station_id
            JOIN users rhq ON r.rhq_user_id = rhq.user_id
            WHERE r.rhq_user_id = %s 
            AND r.status = 'Pending'
            ORDER BY r.created_at DESC
        """

        cursor.execute(query, (rhq_user_id,))
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return rows

    # ------------------------------------------------------
    # STATION — SEE COMPLETE HISTORY
    # ------------------------------------------------------
    @staticmethod
    def get_requests_by_station(station_id: int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                r.*,
                u.name AS requested_by,
                rhq.name AS sent_to_rhq,
                rhq.email AS sent_to_rhq_email
            FROM requests r
            JOIN users u ON r.user_id = u.user_id
            JOIN users rhq ON r.rhq_user_id = rhq.user_id
            WHERE r.station_id = %s
            ORDER BY r.created_at DESC
        """

        cursor.execute(query, (station_id,))
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return rows

    # ------------------------------------------------------
    # UPDATE STATUS (Approve / Reject)
    # ------------------------------------------------------
    @staticmethod
    def update_request_status(request_id: int, status: str,
                              approved_by: int = None, comment: str = None):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE requests 
            SET 
                status = %s,
                rhq_comment = %s,
                approved_by = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE request_id = %s
        """

        cursor.execute(query, (status, comment, approved_by, request_id))
        conn.commit()

        cursor.close()
        conn.close()

    # ------------------------------------------------------
    # GET SINGLE REQUEST — needed for approval page
    # ------------------------------------------------------
    @staticmethod
    def get_request_by_id(request_id: int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                r.*,
                u.name AS requested_by,
                u.email AS requested_by_email,
                s.station_name,
                rhq.name AS rhq_receiver,
                rhq.email AS rhq_receiver_email
            FROM requests r
            JOIN users u ON r.user_id = u.user_id
            JOIN stations s ON r.station_id = s.station_id
            JOIN users rhq ON r.rhq_user_id = rhq.user_id
            WHERE r.request_id = %s
        """

        cursor.execute(query, (request_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()
        return row
