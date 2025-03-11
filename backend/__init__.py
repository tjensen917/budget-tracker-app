from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
import os

# Initialize database
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configure SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///budget_tracker.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models AFTER initializing db
    with app.app_context():
        from backend import models


    # Import models
    from models import Expense, Budget  # Replace with actual class names

    # Register blueprints (routes)
    from routes import main  # Import routes directly
    app.register_blueprint(main)

    return app
