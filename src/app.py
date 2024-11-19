from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_mail import Mail
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from api.utils import APIException, generate_sitemap
from api.models import db
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask extensions
mail = Mail()  # Create mail instance at module level

def create_app():
    app = Flask(__name__)
    
    # Basic config
    app.config.from_object('api.config.Config')
    app.url_map.strict_slashes = False

    # Database configuration
    db_url = os.getenv("DATABASE_URL")
    if db_url is not None:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

# Environment configuration
ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../public/')

# Setup migrations
migrate = Migrate(app, db, compare_type=True)

# Setup admin and commands
setup_admin(app)
setup_commands(app)

# Register blueprint
app.register_blueprint(api)

# Error handler
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Routes
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
    response.cache_control.max_age = 0  # avoid cache memory
    return response

# Run the application
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)