import axios from "axios";


const API_URL = "https://budget-tracker-app-backend-njxe.onrender.com";

export const addExpense = async (expenseData) => {
  console.log("Sending expense data to backend:", {
    user_id: expenseData.user_id || "test-user",
    name: expenseData.name,
    amount: parseFloat(expenseData.amount),
    category: expenseData.category,
    date: expenseData.date,
  });
  return await axios.post(`${API_URL}/add-expense`, {
      user_id: expenseData.user_id || "test-user",  // Ensure this is included
      name: expenseData.name,
      amount: parseFloat(expenseData.amount),  // Convert to float
      category: expenseData.category,
      date: expenseData.date
  });
};

export const getExpenses = (monthYear, userId) => 
  axios.get(`${API_URL}/expenses/${monthYear}`, { params: { user_id: userId } });

export const editExpense = (expenseId, updatedExpense, userId) =>
  axios.put(`${API_URL}/edit-expense/${expenseId}`, { ...updatedExpense, user_id: userId });

export const deleteExpense = (expenseId, userId) =>
  axios.delete(`${API_URL}/delete-expense/${expenseId}`, { params: { user_id: userId } });

export const updateBudget = (newBudget, userId) =>
  axios.put(`${API_URL}/update-budget`, { total_budget: parseFloat(newBudget), user_id: userId });

export const getBudget = (userId) => 
  axios.get(`${API_URL}/budget`, { params: { user_id: userId } });
