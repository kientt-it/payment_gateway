import os
import subprocess

def start_ngrok(port):
    """
    Khởi động ngrok trên cổng cụ thể.
    """
    try:
        command = f'ngrok http {port}'
        process = subprocess.Popen(command, shell=True)
        print(f"Ngrok started on port {port}. Check public URL.")
        return process
    except Exception as e:
        print(f"Error starting ngrok: {e}")
        return None

def start_app(app_command):
    """
    Khởi động ứng dụng của bạn.
    """
    try:
        process = subprocess.Popen(app_command, shell=True)
        print(f"Application started with command: {app_command}")
        return process
    except Exception as e:
        print(f"Error starting application: {e}")
        return None

if __name__ == "__main__":
    app_port = 5000  # Cổng của ứng dụng
    app_script = "sepay.py"  # Tên file ứng dụng của bạn
    app_command = f"python {app_script}"  # Lệnh chạy app

    # Khởi chạy ứng dụng
    app_process = start_app(app_command)

    # Khởi chạy ngrok
    ngrok_process = start_ngrok(app_port)

    # Thông báo kiểm tra ngrok dashboard
    print("Ngrok Dashboard: http://127.0.0.1:4040")

    # Đảm bảo tiến trình chạy mãi mãi
    try:
        # Chờ ứng dụng hoặc ngrok kết thúc (giữ tiến trình chạy)
        app_process.wait()
        ngrok_process.wait()
    except KeyboardInterrupt:
        print("Shutting down...")
        app_process.terminate()
        ngrok_process.terminate()
