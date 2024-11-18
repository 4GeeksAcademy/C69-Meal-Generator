# app.py
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_mail import Mail
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from api.utils import APIException, generate_sitemap
from api.models import db
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
import os

app = Flask(__name__)
mail = Mail()  # Create mail instance at module level

def create_app():
    # Basic config
    app.config.from_object('api.config.Config')

    # Mail config
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.getenv('GMAIL')
    app.config['MAIL_PASSWORD'] = os.getenv('GMAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = ('Personal TOWA Menu', 'towa69devteam@gmail.com')

    # Initialize extensions
    mail.init_app(app)
    JWTManager(app)
    db.init_app(app)
    
    return app

# Create and configure app
app = create_app()

# Rest of your existing configuration...
ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../public/')

# Database configuration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db, compare_type=True)

# Setup admin and commands
setup_admin(app)
setup_commands(app)

# Register blueprint
app.register_blueprint(api)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0
    return response

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)

# from flask import Flask, request, jsonify, url_for, send_from_directory
# from flask_mail import Mail
# from flask_migrate import Migrate
# from flask_jwt_extended import JWTManager
# from api.utils import APIException, generate_sitemap
# from api.models import db
# from api.routes import api
# from api.admin import setup_admin
# from api.commands import setup_commands
# import os

# app = Flask(__name__)

# # Basic config
# app.config.from_object('api.config.Config')

# # Mail config
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_USERNAME'] = os.getenv('GMAIL')
# app.config['MAIL_PASSWORD'] = os.getenv('GMAIL_PASSWORD')
# app.config['MAIL_DEFAULT_SENDER'] = ('Personal TOWA Menu', 'towa69devteam@gmail.com')

# # Initialize extensions
# mail = Mail(app)
# # """
# # This module takes care of starting the API Server, Loading the DB and Adding the endpoints
# # """
# # import os
# # from flask import Flask, request, jsonify, url_for, send_from_directory
# # from flask_migrate import Migrate
# # from flask_swagger import swagger
# # from flask_mail import Mail
# # from api.utils import APIException, generate_sitemap
# # from api.models import db
# # from api.routes import api
# # from api.admin import setup_admin
# # from api.commands import setup_commands
# # from flask_jwt_extended import JWTManager
# # from api.config import Config
# # from api.email_setup import init_mail

# # def create_app():
# #     app = Flask(__name__)
# #     app.config.from_object(Config)

# #     app.config.update(
# #         MAIL_SERVER='smtp.gmail.com',  # Replace with your SMTP server
# #         MAIL_PORT=587,
# #         MAIL_USE_TLS=True,
# #         MAIL_USE_SSL=False,
# #         MAIL_USERNAME=os.getenv("GMAIL"),
# #         MAIL_PASSWORD=os.getenv("GMAIL_PASSWORD"),
# #         MAIL_DEFAULT_SENDER=('Personal TOWA Menu', 'towa69devteam@gmail.com')
# #     )

# #     mail = Mail(app)

# #     return app, mail

# # from models import Person

# ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
# static_file_dir = os.path.join(os.path.dirname(
#     os.path.realpath(__file__)), '../public/')
# app = Flask(__name__)
# JWTManager(app)
# app.url_map.strict_slashes = False

# # database condiguration
# db_url = os.getenv("DATABASE_URL")
# if db_url is not None:
#     app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
#         "postgres://", "postgresql://")
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# MIGRATE = Migrate(app, db, compare_type=True)
# db.init_app(app)

# # add the admin
# setup_admin(app)

# # add the admin
# setup_commands(app)

# app.register_blueprint(api)

# # Handle/serialize errors like a JSON object


# @app.errorhandler(APIException)
# def handle_invalid_usage(error):
#     return jsonify(error.to_dict()), error.status_code

# # generate sitemap with all your endpoints


# @app.route('/')
# def sitemap():
#     if ENV == "development":
#         return generate_sitemap(app)
#     return send_from_directory(static_file_dir, 'index.html')

# # any other endpoint will try to serve it like a static file


# @app.route('/<path:path>', methods=['GET'])
# def serve_any_other_file(path):
#     if not os.path.isfile(os.path.join(static_file_dir, path)):
#         path = 'index.html'
#     response = send_from_directory(static_file_dir, path)
#     response.cache_control.max_age = 0  # avoid cache memory
#     return response


# # this only runs if `$ python src/main.py` is executed
# if __name__ == '__main__':
#     PORT = int(os.environ.get('PORT', 3001))
#     app.run(host='0.0.0.0', port=PORT, debug=True)
