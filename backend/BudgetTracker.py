# Title: Budget Tracker
# Author: Tyler Jensen
# Date: November 4, 2024
# Description: This program calculates your monthly budget

# Notes: Change the budget on line 21 before running to your liking

# App Requirements: 
#   User enters expense
#   Save expense to CSV file
#   Summarize expense totals
#   Show remaining budget

from backend.expense import Expense
import datetime
import calendar
import os

def main():
    
    print(f"Running Budget Tracker!")
    expense_file_path = "expenses.csv"
    budget = 2000

    #Resets the budget if new month
    budget = reset_budget(expense_file_path, budget)

    # Get user input for expense
    expense = get_user_expense()

    # Write their expense to a file
    save_expense_to_file(expense, expense_file_path)
    
    # Read dile and summarize expenses
    summarize_expenses(expense_file_path, budget)

    #Call this function when user requests past data
    month_input = input("Enter month-year (YYYY-MM) to view history or press Enter to skip: ")
    if month_input:
        view_expense_history(month_input, expense_file_path)


def get_user_expense():
    print(f"getting user expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    expense_categories = [
        "Food",
        "Home",
        "Work",
        "Fun",
        "Miscellaneous"
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"    {i+1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1
        # Needs error handling using Try for catching non-ints

        if i in range(len(expense_categories)):
            
            selected_category = expense_categories[selected_index]
            
            new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)
           
            return new_expense
        
        else:
            print("Invalid category. Please try again!")



def save_expense_to_file(expense : Expense, expense_file_path):
    now = datetime.datetime.now()
    month_year = now.strftime("%Y-%m")
    
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category},{month_year}\n")
    
def reset_budget(expense_file_path, budget):
    now = datetime.datetime.now()
    current_month = now.strftime("%Y-%m")

    new_budget = None #default to None if no reset is needed

    if os.path.exists(expense_file_path):
        with open(expense_file_path, "r") as f:
            lines = f.readlines()
            if lines:
                last_entry = lines[-1]
                _,_, last_month = last_entry.strip().split(",")

                if last_month != current_month:
                    print("New month detected! Resetting budget...")
                    os.rename(expense_file_path, f"expenses_{last_month}.csv")
                    open(expense_file_path, "w").close() #Creates a new empty file for the month
                    new_budget = budget #Reset budget for the new month

    return new_budget if new_budget is not None else budget

def summarize_expenses(expense_file_path, budget):
    print(f"summarizing user expense")
    expenses: list[Expense] = []
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(name=expense_name, amount=float(expense_amount), category=expense_category)
            expenses.append(line_expense)
    
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses By Category: ")
    for key, amount in amount_by_category.items():
        print(f"    {key}: ${amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"You've spent ${total_spent:.2f} this month!")
    
    remaining_budget = budget - total_spent
    # Determine what to do/say when exceeding budget
    if remaining_budget > 0:
        print(yellow(f"Budget Remaining: ${remaining_budget:.2f}"))
    else:
        print(red(f"Budget Remaining: ${remaining_budget:.2f}"))
    # Get the current date
    now = datetime.datetime.now()
    # Get number of days in current month
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    # Calculate the remaining number of days in the current month
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    if daily_budget > 0:
        print(green(f"Budget per day: ${daily_budget:.2f}"))
    else:
        print(red(f"Budget per day: ${daily_budget:.2f}"))


def view_expense_history(month_year, expense_file_path):
    print(f"Showing expenses for {month_year}:")
    try:
        with open(expense_file_path, "r") as f:
            lines = f.readlines()
            filtered_expenses = [
                line.strip() for line in lines if line.strip().endswith(month_year)
            ]
            if filtered_expenses:
                for expense in filtered_expenses:
                    print(expense)
            else:
                print("No expenses found for this month.")
    except FileNotFoundError:
        print("No expense history available.")


# Change text color to make dollar amounts stand out
def green(text):
    return f"\033[92m{text}\033[0m"
def blue(text):
    return f"\033[34m{text}\033[0m"
def red(text):
    return f"\033[31m{text}\033[0m"
def yellow(text):
    return f"\033[33m{text}\033[0m"

if __name__ == "__main__":
    main()
