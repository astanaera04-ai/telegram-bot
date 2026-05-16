import json
import os

DATA_FILE = "expenses.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

expenses = load_data()

while True:
    name = input("Enter expense name (or type 'quit'): ")
    if name.lower() == 'quit': break
    amount = float(input("Enter amount: "))
    expenses.append({"name": name, "amount": amount})

save_data(expenses)

total = sum(e['amount'] for e in expenses)
print(f"\nTotal Spending: ${total:.2f}")

if expenses:
    largest = max(expenses, key=lambda x: x['amount'])
    print(f"Largest Expense: {largest['name']} (${largest['amount']})")

    limit = 50
    print(f"Expenses above ${limit}: {[e['name'] for e in expenses if e['amount'] > limit]}")