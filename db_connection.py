
import mysql.connector
import pandas as pd

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="financial"
    )

def get_monthly_summary():
    query = """
        SELECT
            DATE_FORMAT(transaction_date, '%Y-%m-01') AS month,
            SUM(IF(transaction_type = 'revenue', amount, 0))
                AS total_revenue,
            SUM(IF(transaction_type = 'expense', amount, 0))
                AS total_expenses,
            SUM(
                IF(transaction_type = 'revenue', amount,
                   IF(transaction_type = 'expense', -amount, 0))
            ) AS net_profit
        FROM transactions
        GROUP BY
            YEAR(transaction_date),
            MONTH(transaction_date),
            DATE_FORMAT(transaction_date, '%Y-%m-01')
        ORDER BY month;
    """

    conn = get_connection()
    try:
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()


if __name__ == "__main__":
    print(get_monthly_summary())
