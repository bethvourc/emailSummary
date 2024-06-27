import smtplib
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# Email configuration
sender_email = "youremail@example.com"
receiver_email = "receiver@example.com"
password = "yourpassword"
# server used to send the email (e.g. yahoo mail, gmail,...)
smtp_server = "smtp.gmail.com" 
smtp_port = 587

# Path to the report
report_path = "path/to/your/report.csv"

def send_email():
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Daily Report"

    # Email body
    body = "Please find the daily report attached."
    msg.attach(MIMEText(body, 'plain'))

    # Attach the report
    attachment = open(report_path, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(report_path)}")
    msg.attach(part)

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Schedule the email to be sent daily at a specific time
schedule.every().day.at("08:00").do(send_email)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
