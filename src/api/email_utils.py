from flask_mail import Message
from flask import current_app
import os
from api.email_setup import mail  # Import from email_setup instead of app

def send_reset_email(email, token):
    try:
        reset_link = f"{os.getenv('FRONTEND_URL')}/reset-password?token={token}"
        msg = Message(
            "TOWA's Interactive Menu Password Reset",
            sender=('Personal TOWA Menu', 'towa69devteam@gmail.com'),
            recipients=[email]
        )
        msg.body = f"""
        Hello,
        
        You are receiving this email because you requested to reset your password.
        To reset your password, click on the link below:
        {reset_link}
        
        This link will expire in 30 minutes.
        
        If you did not place this request, ignore this message.
        
        Happy Eating,
        TOWA TEAM
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Detailed error: {str(e)}")
        return False

# -------------------------------
# from flask_mail import Message
# from flask import current_app as app
# import os

# def send_reset_email(email, token):
#     try:
#         reset_link = f"{os.getenv('FRONTEND_URL')}/reset-password?token={token}"
#         with app.mail.connect() as conn:
#             msg = Message(
#                 "TOWA's Interactive Menu Password Reset",
#                 sender=('Personal TOWA Menu', 'towa69devteam@gmail.com'),
#                 recipients=[email]
#             )
#             msg.body = f"""
#             Hello,
            
#             You are receiving this email because you requested to reset your password.
#             To reset your password, click on the link below:
#             {reset_link}
            
#             This link will expire in 30 minutes.
            
#             If you did not place this request, ignore this message.
            
#             Happy Eating,
#             TOWA TEAM
#             """
#             conn.send(msg)
#         return True
#     except Exception as e:
#         print(f"Detailed error: {str(e)}")
#         return False
        
# --------------------
# from flask_mail import Message
# from api.email_setup import mail
# import os

# def send_reset_email(email, token):
#     try:
#         reset_link = f"{os.getenv('FRONTEND_URL')}/reset-password?token={token}"
#         msg = Message(
#             subject="TOWA's Interactive Menu Password Reset",
#             sender=os.getenv("GMAIL"),
#             recipients=[email]
#         )
#         msg.body = f"""
#         Hello,
        
#         You are receiving this email because you requested to reset your password.
#         To reset your password, click on the link below:
#         {reset_link}
        
#         This link will expire in 30 minutes.
        
#         If you did not place this request, ignore this message.
        
#         Happy Eating,
#         TOWA TEAM
#         """
#         mail.send(msg)
#         return True
#     except Exception as e:
#         print(f"Detailed error: {str(e)}")
#         return False

# ------------------------------------------
# from flask_mail import Message;
# from api.email_setup import mail;
# import os

# def send_reset_email(email, token):
#     try:

#         reset_link = f"{os.getenv('FRONTEND_URL')}/reset-password?token={token}"
#         subject = "TOWA's Interactive Menu Password Reset"
#         body = f"""
#         Hello, 
        
#         You are recieving this email because you have requested to reset your password.
#         To reset your password, click on the link below:
#         {reset_link}
#         This link will expire in 30 minutes.
        
#         If you did not place this request, ignore this message and continue to use your current password.
        
#         Happy Eating, 
#         TOWA TEAM
#         """

#         print(f"Attempting to send email to {email}")
#         print(f"Using mail instance: {mail}")
#         msg = Message(subject, recipients=[email], body=body)
#         mail.send(msg)
#         print("Email sent successfully.")
#         return True

#     except Exception as e:
#         print (f"Error sending email: {e} ")
#         return False