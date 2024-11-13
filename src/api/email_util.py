from flask_mail import Message;
from mail_setup import mail;

def send_reset_email(email, token):
    reset_link = "https://glorious-system-r4r4jxvpw7rwf5ppj-3000.app.github.dev/reset-password?token={token}"
    subject = "TOWA's Interactive Menu Password Reset"
    body = f"""
    Hello, 
    
    You are recieving this email because you have requested to reset your password.
    To reset your password, click on the link below:
    {reset_link}
    This link will expire in 30 minutes.
    
    If you did not place this request, ignore this message and continue to use your current password.
    
    Happy Eating, 
    TOWA TEAM
    """