import requests

def generate_vietqr_via_api():
    # URL và headers
    url = "https://dev.vietqr.org/vqr/api/qr/generate-customer"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer <token>"  # Thay bằng token bạn nhận được
    }

    # Dữ liệu gửi lên API
    payload = {
        "bankCode": "970418",  # Mã ngân hàng BIDV
        "bankAccount": "8840044593",  # Số tài khoản nhận
        "userBankName": "TRAN TRUNG KIEN",  # Tên chủ tài khoản
        "content": "Thanh toan don hang #12345",  # Nội dung thanh toán
        "qrType": 0,  # VietQR động
        "amount": 100000,  # Số tiền thanh toán
        "orderId": "12345"  # Mã đơn hàng (tùy chọn)
    }

    # Gửi yêu cầu POST
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        # Xử lý phản hồi từ API
        response_data = response.json()
        if "qrData" in response_data:
            qr_data = response_data["qrData"]
            print("Nội dung QR Code:", qr_data)
            
            # Render mã QR
            render_qr_code(qr_data)
        else:
            print("Phản hồi không chứa 'qrData'")
    else:
        print(f"Lỗi khi gọi API: {response.status_code}, {response.text}")

def render_qr_code(qr_data):
    import qrcode

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Lưu mã QR
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("vietQR.png")
    print("QR Code đã được lưu tại vietQR.png")

# Gọi hàm tạo QR
generate_vietqr_via_api()
