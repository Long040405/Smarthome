import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config

def send_warning_email():
    """Connects to SMTP and sends a security warning email."""
    try:
        # Create the MIME message
        message = MIMEMultipart()
        message["From"] = config.SENDER_EMAIL
        message["To"] = config.RECIPIENT_EMAIL
        message["Subject"] = "Cảnh Báo: Đăng Nhập Quá Nhiều Lần"

        # Email content
        body = """\
Chào bạn,

Hệ thống đã phát hiện số lượng đăng nhập không hợp lệ quá mức cho phép.

Nếu bạn không thực hiện các hoạt động đăng nhập này, vui lòng liên hệ với bộ phận hỗ trợ ngay lập tức.

Cảm ơn bạn,
~Nhóm LoNi2H~
"""
        message.attach(MIMEText(body, "plain"))

        # Connect and send
        server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
        server.starttls()
        server.login(config.SENDER_EMAIL, config.SENDER_PASSWORD)
        server.send_message(message)
        server.quit()
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
