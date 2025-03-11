from flask import Flask
from config import Config
from app import db  # Import db from app instead of backend
from models import Expense, Budget  # Ensure this is correct
from routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(main)

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
