import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Route hiển thị form để nhập thông tin thanh toán
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        account_number = request.form.get('account_number') # Số tài khoản ngân hàng (VA)
        bank = request.form.get('bank') # Mã ngân hàng
        amount = request.form.get('amount')  # Số tiền cần chuyển
        description = request.form.get('description')  # Nội dung thanh toán

        # Chuyển đến trang hiển thị mã QR
        return render_template('qr_code.html', account_number = account_number, bank = bank, amount=amount, description=description)

    # Hiển thị form nếu là GET request
    return render_template('index.html')


# Route hiển thị QR Code
@app.route('/qr_code', methods=['POST', 'GET'])
def display_qr_code():
    # Lấy dữ liệu từ form POST hoặc query string
    account_number = request.args.get('account_number', "96247BOLJN")  
    bank = request.args.get('bank', "BIDV") 
    amount = request.args.get('amount', "") 
    description = request.args.get('description', "") 
    
    # URL QR Code động
    qr_url = f"https://qr.sepay.vn/img?acc={account_number}&bank={bank}&amount={amount}&des={description}"

    # Hiển thị trang QR Code
    return render_template('qr_code.html', qr_url=qr_url, account_number = account_number, bank = bank, amount=amount, description=description)


# Route xử lý callback từ API
@app.route('/callback', methods=['POST'])
def callback():
    # Lấy dữ liệu từ callback (giả sử API gửi JSON)
    data = request.json
    print("Callback received:", data)  # Log dữ liệu callback để kiểm tra

    # Trích xuất thông tin từ dữ liệu callback
    user = data.get('user', 'test')  # Giả sử API trả trường user
    name = data.get('name', 'Test')  # Giả sử API trả trường name

    # Xử lý hoặc lưu thông tin người thanh toán
    return jsonify({
        "status": "success",
        "message": "Thông tin thanh toán đã nhận",
        "user": user,
        "name": name
    })


@app.route('/webhook', methods=['POST'])
def sepay_webhook():
    """
    Xử lý webhook từ Sepay.
    """
    try:
        # Lấy dữ liệu JSON từ webhook
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        # Kiểm tra API Key nếu Sepay yêu cầu
        api_key = request.headers.get('Authorization')
        if api_key != "9QO8RIQXABLNWF3RK4EVEZRJNCYLSGMPAI1S7TTGQCMBJF3OJAMCUUHGE9SJD4QP":
            return jsonify({"error": "Unauthorized"}), 403

        # Log dữ liệu nhận được
        print("Webhook received:", data)

        # Trích xuất thông tin
        transaction_id = data.get("id")
        gateway = data.get("gateway")
        transaction_date = data.get("transactionDate")
        account_number = data.get("accountNumber")
        transfer_type = data.get("transferType")
        transfer_amount = data.get("transferAmount")
        reference_code = data.get("referenceCode")
        content = data.get("content")

        # Xử lý giao dịch tiền vào
        if transfer_type == "in":
            print(f"Nhận tiền vào tài khoản {account_number} từ {gateway}")
            print(f"Số tiền: {transfer_amount}, Nội dung: {content}")
            print(f"Mã giao dịch: {transaction_id}, Mã tham chiếu: {reference_code}")
            return jsonify({"message": "Transaction processed successfully"}), 200

        # Xử lý giao dịch khác
        else:
            print(f"Giao dịch khác: {transaction_id}")
            return jsonify({"message": "Transaction type not supported"}), 200

    except Exception as e:
        print("Error processing webhook:", e)
        return jsonify({"error": "An error occurred"}), 500

# Route xử lý trang thông báo thanh toán thành công
@app.route('/payment_success', methods=['GET'])
def payment_success():
    # Nhận thông tin từ query string (nếu cần)
    transaction_id = request.args.get('transaction_id', "Unknown")
    amount = request.args.get('amount', "0")

    # Hiển thị trang thông báo
    return f"""
    <html>
        <head><title>Thanh toán thành công</title></head>
        <body>
            <h1>Thanh toán thành công!</h1>
            <p>Mã giao dịch: {transaction_id}</p>
            <p>Số tiền: {amount} VND</p>
            <a href="/">Quay lại trang chính</a>
        </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
