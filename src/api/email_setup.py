from flask_mail import Mail

mail = Mail()  # Create the mail instance

def init_mail(app):
    mail.init_app(app)  # Initialize Flask-Mail with the Flask app configuration
    return mail