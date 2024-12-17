from flask import Flask, request, render_template, send_file
import qrcode

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Render form HTML

@app.route('/generate', methods=['POST'])
def generate_qr():
    # Lấy thông tin từ form
    amount = request.form['amount']
    content = request.form['content']
    bank_account = request.form['bank_account']
    bank_code = request.form['bank_code']
    user_bank_name = request.form['user_bank_name']
    
    # Dữ liệu QR Code
    qr_data = (
        f"00020101021138580010A00000072701280006970418"
        f"0114SPVN15{len(bank_code):02}{bank_code}"  # Mã ngân hàng
        f"0208QRIBFTTA"  # Loại QR
        f"5303704"  # Loại tiền tệ VND
        f"540{len(amount):02}{amount}"  # Số tiền
        f"5802VN6217{len(content):02}{content}"  # Nội dung thanh toán
        f"6304"
    )

    # Tính CRC16 checksum
    checksum = calculate_crc16(qr_data)
    qr_data += checksum

    # Tạo QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Lưu QR code thành file
    qr_image_path = "images/generated_vietqr.png"
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(qr_image_path)

    return send_file(qr_image_path, mimetype='image/png', as_attachment=True, download_name='vietQR.png')

def calculate_crc16(data):
    """
    Tính CRC16 checksum
    """
    crc = 0xFFFF
    for byte in data.encode("utf-8"):
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0x8408
            else:
                crc >>= 1
    return f"{crc & 0xFFFF:04X}"

if __name__ == '__main__':
    app.run(debug=True)
