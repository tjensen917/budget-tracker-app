import React, { useState } from "react";
import { addExpense } from "../services/api";

const ExpenseForm = ({ onExpenseAdded }) => {
    const [expense, setExpense] = useState({
        name: "",
        amount: "",
        category: "",
        date: "",
    });

    const handleSubmit = async (e) => {
        e.preventDefault();

        const expenseWithUser = {
            ...expense,
            user_id: "test-user", // Replace with actual user ID logic later
        };

        try {
            await addExpense(expenseWithUser);
            setExpense({
                name: "",
                amount: "",
                category: "",
                date: "",
            });
            onExpenseAdded(); // Refresh expense list
        } catch (error) {
            console.error("Failed to add expense:", error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Expense Name"
                value={expense.name}
                onChange={(e) =>
                    setExpense({ ...expense, name: e.target.value })
                }
                required
            />
            <input
                type="number"
                placeholder="Amount"
                value={expense.amount}
                onChange={(e) =>
                    setExpense({ ...expense, amount: e.target.value })
                }
                required
            />
            <select
                value={expense.category}
                onChange={(e) =>
                    setExpense({ ...expense, category: e.target.value })
                }
                required
            >
                <option value="">Select Category</option>
                <option value="Food">Food</option>
                <option value="Groceries">Groceries</option>
                <option value="Gas">Gas</option>
                <option value="Work">Work</option>
                <option value="Fun">Fun</option>
                <option value="Bills">Bills</option>
                <option value="Miscellaneous">Miscellaneous</option>
            </select>
            <label>Date:</label>
            <input
                type="month"
                name="date"
                value={expense.date}
                onChange={(e) =>
                    setExpense({ ...expense, date: e.target.value })
                }
                required
            />
            <button type="submit">Add Expense</button>
        </form>
    );
};

export default ExpenseForm;
