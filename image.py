import qrcode

def generate_vietqr(data):
    """
    Hàm tạo mã QR VietQR từ thông tin đầu vào.
    """
    # Thông tin từ dữ liệu đầu vào
    bank_code = data["bankCode"]  # Mã ngân hàng
    account_number = data["accountNumber"]  # Số tài khoản
    account_name = data["accountName"]  # Tên người thụ hưởng
    amount = f'{int(data["amount"]):.0f}'  # Số tiền
    description = data["description"]  # Nội dung thanh toán

    # Dữ liệu theo chuẩn VietQR
    template = (
        "00020101021138580010A00000072701280006970418"
        f"0114SPVN15{len(bank_code):02}{bank_code}"  # Mã ngân hàng
        f"0208QRIBFTTA"  # Loại QR
        f"5303704"  # Loại tiền tệ VND (704)
        f"540{len(amount):02}{amount}"  # Số tiền
        f"5802VN6217{len(description):02}{description}"  # Nội dung thanh toán
        f"6304"  # CRC16
    )

    # Tính CRC16 checksum
    checksum = calculate_crc16(template)
    qr_data = template + checksum

    # Tạo QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Lưu và hiển thị QR Code
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("vietQR.png")
    print("QR Code đã tạo thành công và lưu tại vietQR.png")

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

# Thông tin đầu vào
data = {
    "bankCode": "970418",  # Mã ngân hàng BIDV
    "accountNumber": "8840044593",  # Số tài khoản
    "accountName": "TRAN TRUNG KIEN",  # Tên người thụ hưởng
    "amount": 100000,  # Số tiền thanh toán
    "description": "Thanh toan hoa don",  # Nội dung giao dịch
    "extraInfo1": "",  # Thông tin thêm (nếu có)
    "extraInfo2": ""
}

# Tạo QR Code
generate_vietqr(data)


# import qrcode

# def generate_vietqr(bank_name, account_number, account_name, amount, description):
#     """
#     Hàm tạo mã QR theo chuẩn VietQR
#     """
#     # Mã ngân hàng và template VietQR
#     bank_code = "970418"  # Mã ngân hàng (VD: BIDV)
#     currency = "704"  # Loại tiền tệ: 704 = VND
    
#     # Chuỗi dữ liệu chuẩn theo EMVCo
#     template = (
#         "00020101021138580010A00000072701280006970418"
#         f"0114SPVN15{len(bank_code):02}{bank_code}"
#         "0208QRIBFTTA"
#         f"5303{currency}540{len(str(amount))}{amount}"
#         f"5802VN6217{len(description):02}{description}"
#         f"6304"
#     )

#     # Tính CRC16 checksum
#     checksum = calculate_crc16(template)
#     qr_data = template + checksum

#     # Tạo QR Code
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_M,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(qr_data)
#     qr.make(fit=True)

#     # Render và lưu ảnh QR Code
#     img = qr.make_image(fill_color="black", back_color="white")
#     img.save("vietQR.png")
#     print(f"QR Code đã tạo thành công và lưu tại vietQR.png")

# def calculate_crc16(data):
#     """Tính CRC16 checksum"""
#     crc = 0xFFFF
#     for byte in data.encode("utf-8"):
#         crc ^= byte
#         for _ in range(8):
#             if crc & 1:
#                 crc = (crc >> 1) ^ 0x8408
#             else:
#                 crc >>= 1
#     return f"{crc & 0xFFFF:04X}"

# # Thông tin tài khoản và giao dịch
# bank_name = "BIDV - Ngân hàng TMCP Đầu tư và Phát triển Việt Nam"
# account_number = "8840044593"
# account_name = "TRAN TRUNG KIEN"
# amount = 120000  # Số tiền (VNĐ)
# description = "TEST"  # Nội dung chuyển khoản

# # Tạo QR Code
# generate_vietqr(bank_name, account_number, account_name, amount, description)

