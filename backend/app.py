from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db) # Ensure migrations are linked

# Import models (if stored separately)
from models import *  # Ensure this is correct based on your folder structure

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

@app.route('/add-expense', methods=['POST'])
def add_expense():
    try:
        data = request.json  # Get JSON data from frontend
        print("Received Data:", data)  # Debugging - Check what's received
        user_id = data.get('user_id')
        category = data.get('category')
        amount = data.get('amount')
        date = data.get('date')

        if not all([user_id, category, amount, date]):
            return jsonify({"error": "Missing required fields"}), 400  # Handle missing data

        new_expense = Expense(user_id=user_id, category=category, amount=amount, date=date)
        db.session.add(new_expense)
        db.session.commit()

        return jsonify({"message": "Expense added successfully"}), 201

    except Exception as e:
        print("Error:", str(e))  # Logs error in Render logs
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@app.route("/expenses/<month_year>", methods=["GET"])
def get_expenses(month_year):
    user_id = request.args.get("user_id")
    expenses = Expense.query.filter_by(date=month_year, user_id=user_id).all()
    return jsonify([{
        "id": e.id, "name": e.name, "amount": e.amount, "category": e.category, "date": e.date
    } for e in expenses])
@app.route("/edit-expense/<int:expense_id>", methods=["PUT"])
def edit_expense(expense_id):
    data = request.json
    expense = Expense.query.filter_by(id=expense_id, user_id=data["user_id"]).first()

    if not expense:
        return jsonify({"message": "Expense not found"}), 404

    expense.name = data.get("name", expense.name)
    expense.amount = data.get("amount", expense.amount)
    expense.category = data.get("category", expense.category)
    
    db.session.commit()
    return jsonify({"message": "Expense updated successfully"})

@app.route("/delete-expense/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    user_id = request.args.get("user_id")
    expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()

    if not expense:
        return jsonify({"message": "Expense not found"}), 404

    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Expense deleted successfully"})

@app.route("/edit-expense/<int:expense_id>", methods=["PUT"])
def edit_expense(expense_id):
    data = request.json
    expense = Expense.query.filter_by(id=expense_id, user_id=data["user_id"]).first()

    if not expense:
        return jsonify({"message": "Expense not found"}), 404

    expense.name = data.get("name", expense.name)
    expense.amount = data.get("amount", expense.amount)
    expense.category = data.get("category", expense.category)
    
    db.session.commit()
    return jsonify({"message": "Expense updated successfully"})

@app.route("/delete-expense/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    user_id = request.args.get("user_id")
    expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()

    if not expense:
        return jsonify({"message": "Expense not found"}), 404

    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Expense deleted successfully"})


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
