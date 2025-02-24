import React, { useState } from "react";
import { editExpense, deleteExpense } from "../services/api";

const ExpenseList = ({ monthYear, expenses }) => {
  const [editingId, setEditingId] = useState(null);
  const [updatedExpense, setUpdatedExpense] = useState({});
  const userId = "user-" + Math.random().toString(36).substr(2, 9); // Simulated unique user

  const handleEditClick = (expense) => {
    setEditingId(expense.id);
    setUpdatedExpense({ ...expense });
  };

  const handleSave = async () => {
    try {
      await editExpense(editingId, updatedExpense, userId);
      alert("Expense updated!");
      window.location.reload();
    } catch (error) {
      console.error("Failed to update expense:", error);
    }
  };

  const handleDelete = async (expenseId) => {
    if (!window.confirm("Are you sure you want to delete this expense?")) return;

    try {
      await deleteExpense(expenseId, userId);
      alert("Expense deleted!");
      window.location.reload();
    } catch (error) {
      console.error("Failed to delete expense:", error);
    }
  };

  return (
    <div>
      <h2>Expenses for {monthYear}</h2>
      {expenses.length === 0 ? (
        <p>No expenses recorded for this month.</p>
      ) : (
        <ul>
          {expenses.map((expense) => (
            <li key={expense.id}>
              {editingId === expense.id ? (
                <>
                  <input
                    type="text"
                    value={updatedExpense.name}
                    onChange={(e) => setUpdatedExpense({ ...updatedExpense, name: e.target.value })}
                  />
                  <input
                    type="number"
                    value={updatedExpense.amount}
                    onChange={(e) => setUpdatedExpense({ ...updatedExpense, amount: parseFloat(e.target.value) })}
                  />
                  <select
                    value={updatedExpense.category}
                    onChange={(e) => setUpdatedExpense({ ...updatedExpense, category: e.target.value })}
                  >
                    <option value="Food">Food</option>
                    <option value="Home">Home</option>
                    <option value="Work">Work</option>
                    <option value="Fun">Fun</option>
                    <option value="Miscellaneous">Miscellaneous</option>
                  </select>
                  <button onClick={handleSave}>Save</button>
                  <button onClick={() => setEditingId(null)}>Cancel</button>
                </>
              ) : (
                <>
                  {expense.name} - ${expense.amount} ({expense.category})
                  <button onClick={() => handleEditClick(expense)}>Edit</button>
                  <button onClick={() => handleDelete(expense.id)} style={{ color: "red" }}>
                    Delete
                  </button>
                </>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ExpenseList;
