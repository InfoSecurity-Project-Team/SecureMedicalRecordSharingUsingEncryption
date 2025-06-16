import smtplib
import random
from email.message import EmailMessage
from datetime import datetime, timedelta
#import string

# Store OTP and timestamp globally
otp_store = {
    'otp': None,
    'timestamp': None
}
def generate_otp():
    otp = ''.join(str(random.randint(0, 9)) for _ in range(6))

#def generate_otp(length=6):
#    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
#    otp = ''.join(random.choices(characters, k=length))
    print("Generated OTP:", otp)
    otp_store['otp'] = otp
    otp_store['timestamp'] = datetime.now()
    return otp

def is_otp_valid(entered_otp, expiration_minutes=5):
    """Check if OTP is valid and not expired (default expiration: 5 minutes)"""
    if otp_store['otp'] is None or otp_store['timestamp'] is None:
        return False

    # Check expiration
    now = datetime.now()
    if now - otp_store['timestamp'] > timedelta(minutes=expiration_minutes):
        return False

    return entered_otp == otp_store['otp']

def send_otp_email(receiver_email, otp):
    sender_email = "smrsystem123@gmail.com"  # Use a real sender
    sender_password = 'rgpp ptvp teal rcbg'

    subject = "Your OTP Code for SMR Authentication"
    print(f"Sending OTP {otp} to {receiver_email}")

    body = f"Your OTP code is: {otp}"

    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email
    message.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            print("smtp login successfull")
            server.send_message(message)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

