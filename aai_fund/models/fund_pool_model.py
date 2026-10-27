# models/fund_pool_model.py
from models.db import get_connection

class FundPoolModel:

    @staticmethod
    def get_pool():
        """
        Fetch the single fund pool record.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT pool_id, total_pool, updated_at FROM fund_pool LIMIT 1")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row


    @staticmethod
    def create_or_set_pool(amount: float):
        """
        Create fund pool if empty, otherwise set the pool amount.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT pool_id FROM fund_pool LIMIT 1")
        row = cursor.fetchone()

        if row:
            # Update existing pool
            cursor.execute("""
                UPDATE fund_pool
                SET total_pool = %s, updated_at = CURRENT_TIMESTAMP
                WHERE pool_id = %s
            """, (amount, row[0]))

        else:
            # Create new pool
            cursor.execute("INSERT INTO fund_pool (total_pool) VALUES (%s)", (amount,))

        conn.commit()
        cursor.close()
        conn.close()


    @staticmethod
    def add_to_pool(amount: float):
        """
        Add amount to the pool.
        Creates pool if it does not exist.
        """
        conn = get_connection()
        cursor = conn.cursor()

        # Ensure only one row exists
        cursor.execute("SELECT pool_id FROM fund_pool LIMIT 1")
        row = cursor.fetchone()

        if row is None:
            # Create pool with initial amount
            cursor.execute("INSERT INTO fund_pool (total_pool) VALUES (%s)", (amount,))
        else:
            # Add new funds to pool
            cursor.execute("""
                UPDATE fund_pool 
                SET total_pool = total_pool + %s, updated_at = CURRENT_TIMESTAMP
                WHERE pool_id = %s
            """, (amount, row[0]))

        conn.commit()
        cursor.close()
        conn.close()


    @staticmethod
    def deduct_from_pool(amount: float) -> bool:
        """
        Deduct amount from pool only if sufficient balance exists.
        Returns:
            True  -> Deduction successful
            False -> Insufficient funds or missing pool
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT pool_id, total_pool FROM fund_pool LIMIT 1")
        row = cursor.fetchone()

        if not row:
            cursor.close()
            conn.close()
            return False

        available = float(row["total_pool"])

        if available < float(amount):
            cursor.close()
            conn.close()
            return False

        # Deduct
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE fund_pool
            SET total_pool = total_pool - %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE pool_id = %s
        """, (amount, row["pool_id"]))

        conn.commit()
        cursor.close()
        conn.close()
        return True
