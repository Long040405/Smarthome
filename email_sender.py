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
        message["Subject"] = "Warning: Too Many Login Attempts"

        # Email content
        body = """\
Hello,

The system has detected an excessive number of invalid login attempts.

If you did not perform these login attempts, please contact support immediately.

Best regards,
~LoNi2H Team~
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
