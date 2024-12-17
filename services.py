import psycopg2

# Cấu hình kết nối PostgreSQL
DB_CONFIG = {
    "host": "localhost",
    "database": "webhooks_receiver",
    "user": "webhooks_receiver",
    "password": "admin",
     "port": 5432 
}

def insert_transaction(data):
    """
    Chèn dữ liệu giao dịch vào PostgreSQL.
    """
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Kiểm tra loại giao dịch tiền vào hay ra
        amount_in = data.get("transferAmount", 0) if data.get("transferType") == "in" else 0
        amount_out = data.get("transferAmount", 0) if data.get("transferType") == "out" else 0

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

        # Log truy vấn để kiểm tra
        print("SQL Query:", cursor.mogrify(sql, values))
        cursor.execute(sql, values)
        connection.commit()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False
    finally:
        if connection:
            connection.close()
