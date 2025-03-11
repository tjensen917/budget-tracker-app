from flask import Blueprint, request, jsonify
from backend import db
from backend.models import Expense, Budget

main = Blueprint('main', __name__)

@main.route('/add-expense', methods=['POST'])
def add_expense():
    data = request.get_json()

    if not data or 'name' not in data or 'amount' not in data or 'user_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    new_expense = Expense(
        user_id=data['user_id'],
        name=data['name'],
        amount=float(data['amount']),
        category=data['category'],
        date=data['date']
    )

    db.session.add(new_expense)
    db.session.commit()
    return jsonify({'message': 'Expense added successfully'}), 201

@main.route("/expenses/<month_year>", methods=["GET"])
def get_expenses(month_year):
    user_id = request.args.get("user_id")
    expenses = Expense.query.filter_by(date=month_year, user_id=user_id).all()
    return jsonify([{
        "id": e.id, "name": e.name, "amount": e.amount, "category": e.category, "date": e.date
    } for e in expenses])

@main.route("/update-budget", methods=["PUT"])
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

@main.route("/budget", methods=["GET"])
def get_budget():
    user_id = request.args.get("user_id")
    budget = Budget.query.filter_by(user_id=user_id).first()
    return jsonify({"total_budget": budget.total_budget}) if budget else jsonify({"total_budget": 0})
