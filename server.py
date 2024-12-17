import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Thông tin kết nối PostgreSQL
DB_CONFIG = {
    "host": "localhost",
    "database": "webhooks_receiver",
    "user": "webhooks_receiver",
    "password": "admin"
}

def insert_transaction(data):
    """
    Chèn dữ liệu giao dịch vào PostgreSQL.
    """
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Kiểm tra loại giao dịch tiền vào hay ra
        amount_in = data["transferAmount"] if data["transferType"] == "in" else 0
        amount_out = data["transferAmount"] if data["transferType"] == "out" else 0

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
            data.get("subAccount"), amount_in, amount_out, data.get("accumulated"),
            data.get("code"), data.get("content"), data.get("referenceCode"), data.get("description")
        )

        # Thực thi truy vấn
        cursor.execute(sql, values)
        connection.commit()

        return True
    except Exception as e:
        print(f"Error inserting transaction: {e}")
        return False
    finally:
        if connection:
            connection.close()

@app.route('/webhook', methods=['POST'])
def sepay_webhook():
    """
    Xử lý webhook từ Sepay.
    """
    try:
        # Lấy dữ liệu JSON từ webhook
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data received"}), 400

        # Lưu dữ liệu giao dịch vào cơ sở dữ liệu
        if insert_transaction(data):
            return jsonify({"success": True, "message": "Transaction saved successfully"}), 200
        else:
            return jsonify({"success": False, "message": "Failed to save transaction"}), 500

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"success": False, "message": "An error occurred"}), 500

if __name__ == "__main__":
    app.run(debug=True)
