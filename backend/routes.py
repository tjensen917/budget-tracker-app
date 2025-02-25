from flask import Blueprint, request, jsonify
from backend import db
from backend.models import Expense, Budget

# Create a Blueprint for API routes
api_bp = Blueprint("api", __name__)

### 📌 ADD EXPENSE ###
@api_bp.route("/add-expense", methods=["POST"])
def add_expense():
    try:
        data = request.json

        # Validate required fields
        if not all(key in data for key in ["user_id", "category", "amount", "date"]):
            return jsonify({"error": "Missing required fields"}), 400

        # Create new expense
        new_expense = Expense(
            user_id=data["user_id"],
            category=data["category"],
            amount=float(data["amount"]),  # Ensure amount is stored as float
            date=data["date"],
        )
        db.session.add(new_expense)
        db.session.commit()

        return jsonify({"message": "Expense added successfully", "expense": {
            "id": new_expense.id,
            "user_id": new_expense.user_id,
            "category": new_expense.category,
            "amount": new_expense.amount,
            "date": new_expense.date
        }}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to add expense", "details": str(e)}), 500

### 📌 GET EXPENSES (For a Specific Month & User) ###
@api_bp.route("/expenses/<month_year>", methods=["GET"])
def get_expenses(month_year):
    try:
        user_id = request.args.get("user_id")

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        expenses = Expense.query.filter_by(date=month_year, user_id=user_id).all()

        return jsonify([{
            "id": e.id,
            "category": e.category,
            "amount": e.amount,
            "date": e.date
        } for e in expenses])

    except Exception as e:
        return jsonify({"error": "Failed to retrieve expenses", "details": str(e)}), 500

### 📌 EDIT EXPENSE ###
@api_bp.route("/edit-expense/<int:expense_id>", methods=["PUT"])
def edit_expense(expense_id):
    try:
        data = request.json
        expense = Expense.query.filter_by(id=expense_id, user_id=data["user_id"]).first()

        if not expense:
            return jsonify({"error": "Expense not found"}), 404

        # Update fields if provided
        expense.category = data.get("category", expense.category)
        expense.amount = float(data.get("amount", expense.amount))

        db.session.commit()
        return jsonify({"message": "Expense updated successfully", "expense": {
            "id": expense.id,
            "category": expense.category,
            "amount": expense.amount,
            "date": expense.date
        }})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update expense", "details": str(e)}), 500

### 📌 DELETE EXPENSE ###
@api_bp.route("/delete-expense/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    try:
        user_id = request.args.get("user_id")
        expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()

        if not expense:
            return jsonify({"error": "Expense not found"}), 404

        db.session.delete(expense)
        db.session.commit()
        return jsonify({"message": "Expense deleted successfully"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete expense", "details": str(e)}), 500

### 📌 UPDATE BUDGET ###
@api_bp.route("/update-budget", methods=["PUT"])
def update_budget():
    try:
        data = request.json
        user_id = data.get("user_id")

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        budget = Budget.query.filter_by(user_id=user_id).first()

        if budget:
            budget.total_budget = float(data["total_budget"])
        else:
            budget = Budget(user_id=user_id, total_budget=float(data["total_budget"]))
            db.session.add(budget)

        db.session.commit()
        return jsonify({"message": "Budget updated successfully", "budget": {
            "user_id": budget.user_id,
            "total_budget": budget.total_budget
        }})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update budget", "details": str(e)}), 500

### 📌 GET BUDGET ###
@api_bp.route("/budget", methods=["GET"])
def get_budget():
    try:
        user_id = request.args.get("user_id")

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        budget = Budget.query.filter_by(user_id=user_id).first()

        return jsonify({"total_budget": budget.total_budget}) if budget else jsonify({"total_budget": 0})

    except Exception as e:
        return jsonify({"error": "Failed to retrieve budget", "details": str(e)}), 500
