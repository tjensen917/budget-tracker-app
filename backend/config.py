import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "theRealWaffleMan")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///instance/budget_tracker.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
