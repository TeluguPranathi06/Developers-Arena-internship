import json
import csv
import os
from datetime import datetime
from collections import defaultdict

DATA_FILE = "expenses.json"
BACKUP_FILE = "expenses_backup.json"

class Expense:
    def __init__(self, date, amount, category, description):
        self.date = self.validate_date(date)
        self.amount = self.validate_amount(amount)
        self.category = category.strip()
        self.description = description.strip()

    def validate_date(self, date):
        try:
            return datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")

    def validate_amount(self, amount):
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        return amount

    def to_dict(self):
        return {
            "date": self.date.isoformat(),
            "amount": self.amount,
            "category": self.category,
            "description": self.description
        }
class ExpenseManager:
    def __init__(self):
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)

    def search_by_category(self, category):
        return [e for e in self.expenses if e.category.lower() == category.lower()]

    def filter_by_month(self, year, month):
        return [e for e in self.expenses if e.date.year == year and e.date.month == month]
def save_expenses(manager):
    with open(DATA_FILE, "w") as file:
        json.dump([e.to_dict() for e in manager.expenses], file, indent=4)


def load_expenses():
    expenses = []
    if not os.path.exists(DATA_FILE):
        return expenses

    with open(DATA_FILE, "r") as file:
        data = json.load(file)
        for item in data:
            expenses.append(Expense(**item))
    return expenses


def backup_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as src, open(BACKUP_FILE, "w") as dest:
            dest.write(src.read())


def export_to_csv(expenses):
    with open("expenses.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=["date", "amount", "category", "description"]
        )
        writer.writeheader()
        for e in expenses:
            writer.writerow(e.to_dict())

def monthly_report(expenses):
    if not expenses:
        print("No expenses found")
        return

    total = sum(e.amount for e in expenses)
    print(f"\nTotal Expense: ₹{total:.2f}")

    category_total = defaultdict(float)
    for e in expenses:
        category_total[e.category] += e.amount

    print("\nCategory-wise Breakdown")
    for cat, amt in category_total.items():
        print(f"{cat:<15} ₹{amt:.2f}")

    print("\nExpense Visualization")
    for cat, amt in category_total.items():
        print(cat, "|" + "█" * int(amt / 100))
def menu():
    print("""
1. Add Expense
2. Monthly Report
3. Search by Category
4. Export to CSV
5. Backup Data
6. Exit
""")
def main():
    manager = ExpenseManager()
    manager.expenses = load_expenses()

    while True:
        menu()
        choice = input("Enter choice: ")

        try:
            if choice == "1":
                date = input("Date (YYYY-MM-DD): ")
                amount = input("Amount: ")
                category = input("Category: ")
                description = input("Description: ")

                expense = Expense(date, amount, category, description)
                manager.add_expense(expense)
                save_expenses(manager)
                print("Expense added successfully")

            elif choice == "2":
                year = int(input("Year: "))
                month = int(input("Month: "))
                monthly = manager.filter_by_month(year, month)
                monthly_report(monthly)

            elif choice == "3":
                cat = input("Category: ")
                results = manager.search_by_category(cat)
                for e in results:
                    print(e.to_dict())

            elif choice == "4":
                export_to_csv(manager.expenses)
                print("Exported to expenses.csv")

            elif choice == "5":
                backup_data()
                print("Backup completed")

            elif choice == "6":
                print("Thank you! Exiting...")
                break

            else:
                print("Invalid choice")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
