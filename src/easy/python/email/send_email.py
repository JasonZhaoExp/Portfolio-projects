import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import argparse

def send_email(to_address, subject, body, attachment_path):
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    from_address = 'your_email@example.com'
    password = 'your_password'

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        try:
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
                msg.attach(part)
        except Exception as e:
            print(f"Error attaching file: {e}")
            return

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_address, password)
        server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send an email with an attachment.')
    parser.add_argument('--to', required=True, help='Recipient email address')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--body', required=True, help='Email body')
    parser.add_argument('--attachment', help='Path to the attachment file')

    print("Usage: python send_email.py --to recipient@example.com --subject 'Subject Here' --body 'Email body here' --attachment 'path/to/file'")

    args = parser.parse_args()
    send_email(args.to, args.subject, args.body, args.attachment)
