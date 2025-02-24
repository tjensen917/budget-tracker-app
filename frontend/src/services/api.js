import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

export const addExpense = (expense, userId) => 
  axios.post(`${API_URL}/add-expense`, { ...expense, user_id: userId });

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
