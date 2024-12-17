import os
import psycopg2

# Cấu hình kết nối PostgreSQL
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", 5432)
}

def insert_transaction(data):
    connection = None
    try:
        # Kết nối tới PostgreSQL
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Chuẩn bị dữ liệu giao dịch
        amount_in = data.get("transferAmount") if data.get("transferType") == "in" else 0
        amount_out = data.get("transferAmount") if data.get("transferType") == "out" else 0

        # Tạo câu truy vấn SQL
        sql = """
            INSERT INTO tb_transactions (
                gateway, transaction_date, account_number, sub_account,
                amount_in, amount_out, accumulated, code, transaction_content,
                reference_number, body
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data.get("gateway"), data.get("transactionDate"), data.get("accountNumber"),
            data.get("subAccount"), amount_in, amount_out, data.get("accumulated", 0),
            data.get("code"), data.get("content"), data.get("referenceCode"), data.get("description")
        )

        cursor.execute(sql, values)
        connection.commit()
        return True

    except psycopg2.OperationalError as e:
        print(f"Database connection error: {e}")
        return False
    except Exception as e:
        print(f"Database error: {e}")
        return False
    finally:
        if connection:
            connection.close()

