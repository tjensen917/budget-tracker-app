from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budget_tracker.db"
db = SQLAlchemy(app)

# Expense Model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)  # Unique user session
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(7), nullable=False)  # YYYY-MM format

# Budget Model
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), unique=True, nullable=False)
    total_budget = db.Column(db.Float, nullable=False)

@app.route("/add-expense", methods=["POST"])
def add_expense():
    data = request.json
    new_expense = Expense(
        user_id=data["user_id"],
        name=data["name"],
        amount=data["amount"],
        category=data["category"],
        date=datetime.now().strftime("%Y-%m"),
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"message": "Expense added successfully"}), 201

@app.route("/expenses/<month_year>", methods=["GET"])
def get_expenses(month_year):
    user_id = request.args.get("user_id")
    expenses = Expense.query.filter_by(date=month_year, user_id=user_id).all()
    return jsonify([{
        "id": e.id, "name": e.name, "amount": e.amount, "category": e.category, "date": e.date
    } for e in expenses])

@app.route("/update-budget", methods=["PUT"])
def update_budget():
    data = request.json
    user_id = data.get("user_id")

    budget = Budget.query.filter_by(user_id=user_id).first()
    if budget:
        budget.total_budget = float(data["total_budget"])
    else:
        budget = Budget(user_id=user_id, total_budget=float(data["total_budget"]))
        db.session.add(budget)

    db.session.commit()
    return jsonify({"message": "Budget updated successfully"})

@app.route("/budget", methods=["GET"])
def get_budget():
    user_id = request.args.get("user_id")
    budget = Budget.query.filter_by(user_id=user_id).first()
    return jsonify({"total_budget": budget.total_budget}) if budget else jsonify({"total_budget": 0})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
