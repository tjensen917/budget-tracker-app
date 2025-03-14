from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/budget_tracker.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions properly
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models **AFTER** db.init_app
    with app.app_context():
        from backend.models import Expense, Budget  # Ensure these models are imported here

    # Register blueprints (routes)
    from backend.routes import main
    app.register_blueprint(main)

    return app
