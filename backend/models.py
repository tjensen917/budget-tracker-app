from app import db
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
class Expense(db.Model):
    __tablename__ = 'expense'
    __table_args__ = {'extend_existing': True}  # This allows existing tables to be reused

    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_budget = db.Column(db.Float, nullable=False)
