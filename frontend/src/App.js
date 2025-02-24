import React, { useEffect, useState } from "react";
import ExpenseForm from "./components/ExpenseForm";
import ExpenseList from "./components/ExpenseList";
import { getBudget, updateBudget, getExpenses } from "./services/api";
import "./styles.css";

const App = () => {
  const [monthYear] = useState(new Date().toISOString().slice(0, 7));
  const [budget, setBudget] = useState(2000);
  const [expenses, setExpenses] = useState([]);
  const [remainingBudget, setRemainingBudget] = useState(2000);
  const [totalExpenses, setTotalExpenses] = useState(0);
  const [budgetUsedPercent, setBudgetUsedPercent] = useState("BaNaNas");
  const [showBudgetInput, setShowBudgetInput] = useState(false);
  const [newBudget, setNewBudget] = useState("");
  const [imagesToShow, setImagesToShow] = useState(5);

  const userId = "user-" + Math.random().toString(36).substr(2, 9); // Simulated unique user

  useEffect(() => {
    const fetchData = async () => {
      try {
        const budgetResponse = await getBudget(userId);
        setBudget(budgetResponse.data.total_budget);

        const expensesResponse = await getExpenses(monthYear, userId);
        setExpenses(expensesResponse.data);

        const totalExpensesAmount = expensesResponse.data.reduce((sum, exp) => sum + exp.amount, 0);
        setTotalExpenses(totalExpensesAmount);
        setRemainingBudget(budgetResponse.data.total_budget - totalExpensesAmount);

        let usedPercent = (totalExpensesAmount / budgetResponse.data.total_budget) * 100;
        if (!budgetResponse.data.total_budget || isNaN(usedPercent) || !isFinite(usedPercent)) {
          usedPercent = "BaNaNas";
        } else {
          usedPercent = usedPercent.toFixed(2) + "%";
        }

        setBudgetUsedPercent(usedPercent);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    fetchData();
  }, [monthYear]);

  useEffect(() => {
    let imagesCount = 5;
    if (budgetUsedPercent !== "BaNaNas") {
      const percentValue = parseFloat(budgetUsedPercent);
      if (percentValue >= 80) imagesCount = 1;
      else if (percentValue >= 60) imagesCount = 2;
      else if (percentValue >= 40) imagesCount = 3;
      else if (percentValue >= 20) imagesCount = 4;
      else if (percentValue > 100) imagesCount = 0;
    }
    setImagesToShow(imagesCount);
  }, [budgetUsedPercent]);

  const handleUpdateBudget = async () => {
    try {
      if (!newBudget) {
        alert("Please enter a budget amount.");
        return;
      }

      await updateBudget(newBudget, userId);
      setBudget(newBudget);
      setRemainingBudget(newBudget - totalExpenses);

      let usedPercent = (totalExpenses / newBudget) * 100;
      if (!newBudget || isNaN(usedPercent) || !isFinite(usedPercent)) {
        usedPercent = "BaNaNas";
      } else {
        usedPercent = usedPercent.toFixed(2) + "%";
      }

      setBudgetUsedPercent(usedPercent);

      setNewBudget("");
      setShowBudgetInput(false);
      alert("Budget updated successfully!");
    } catch (error) {
      alert("Failed to update budget. Check console.");
    }
  };

  return (
    <div>
      <h1>Black Bananas Budget</h1>

      <div className="favicon-container">
        {budgetUsedPercent !== "BaNaNas" && parseFloat(budgetUsedPercent) > 100 ? (
          <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "20px" }}>
            <img src="/over-budget.png" alt="Over Budget" style={{ width: "64px" }} />
            <h2 style={{ color: "rgb(97, 97, 231)" }}> Over Budget! </h2>
            <img src="/over-budget.png" alt="Over Budget" style={{ width: "64px" }} />
          </div>
        ) : (
          [...Array(imagesToShow)].map((_, index) => (
            <img key={index} src="/bigFavicon.png" alt="Budget Icon" style={{ width: "64px", marginRight: "10px" }} />
          ))
        )}
      </div>

      <h2>Total Budget: ${budget}</h2>
      <h3>Total Expenses: ${totalExpenses}</h3>
      <h3>Remaining Budget: ${remainingBudget}</h3>
      <h3>Budget Used: {budgetUsedPercent === "BaNaNas" ? "BaNaNas" : budgetUsedPercent}</h3>

      {showBudgetInput ? (
        <>
          <input type="number" value={newBudget} onChange={(e) => setNewBudget(e.target.value)} />
          <button onClick={handleUpdateBudget}>Save</button>
        </>
      ) : (
        <button onClick={() => setShowBudgetInput(true)}>Update Budget</button>
      )}

      <ExpenseForm />
      <ExpenseList expenses={expenses} />
    </div>
  );
};

export default App;
