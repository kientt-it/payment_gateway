from flask import Blueprint, request, jsonify, render_template
from services import insert_transaction

# Khởi tạo Blueprint
routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET', 'POST'])
def index():
    """
    Hiển thị form nhập thông tin thanh toán và tạo mã QR.
    """
    if request.method == 'POST':
        account_number = request.form.get('account_number')
        bank = request.form.get('bank')
        amount = request.form.get('amount')
        description = request.form.get('description')

        return render_template('qr_code.html', account_number=account_number, bank=bank, amount=amount, description=description)

    return render_template('index.html')

@routes.route('/qr_code', methods=['POST', 'GET'])
def display_qr_code():
    """
    Hiển thị QR Code dựa trên thông tin nhập vào.
    """
    account_number = request.args.get('account_number', "96247BOLJN")
    bank = request.args.get('bank', "BIDV")
    amount = request.args.get('amount', "")
    description = request.args.get('description', "")

    qr_url = f"https://qr.sepay.vn/img?acc={account_number}&bank={bank}&amount={amount}&des={description}"

    return render_template('qr_code.html', qr_url=qr_url, account_number=account_number, bank=bank, amount=amount, description=description)

@routes.route('/webhook', methods=['POST'])
def sepay_webhook():
    """
    Xử lý webhook từ Sepay và lưu dữ liệu vào cơ sở dữ liệu.
    """
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data received"}), 400

        print("Webhook Data Received:", data)

        if insert_transaction(data):
            return jsonify({"success": True, "message": "Transaction saved successfully"}), 200
        else:
            return jsonify({"success": False, "message": "Failed to save transaction"}), 500

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"success": False, "message": "An error occurred"}), 500

@routes.route('/callback', methods=['POST'])
def callback():
    """
    Xử lý callback từ API.
    """
    data = request.json
    print("Callback received:", data)

    user = data.get('user', 'test')
    name = data.get('name', 'Test')

    return jsonify({
        "status": "success",
        "message": "Thông tin thanh toán đã nhận",
        "user": user,
        "name": name
    })

@routes.route('/payment_success', methods=['GET'])
def payment_success():
    """
    Hiển thị thông báo khi thanh toán thành công.
    """
    transaction_id = request.args.get('transaction_id', "Unknown")
    amount = request.args.get('amount', "0")

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
