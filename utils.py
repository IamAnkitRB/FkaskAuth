import random
from flask_mail import Message

def generate_otp():
    """Generate a 6-digit OTP."""
    return f"{random.randint(100000, 999999)}"

def send_otp(email, otp, mail):
    """Send OTP to the user's email."""
    try:
        msg = Message('Your OTP Code', sender=mail.app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = f"Your OTP is: {otp}"
        mail.send(msg)
    except Exception as e:
        print(f"Error sending OTP: {e}")
        raise
