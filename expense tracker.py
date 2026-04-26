
# add/ view/ delete expenses
# monthly summaries and insight
# save/ load from JSON file

import json
import os
from datetime import datetime

data_file = "expense.json"
categories = [
    "food",
    "health",
    "housing",
    "transportation",
    "entertainment",
    "other",
]

# file I/O
def load_expense():
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            return json.load(f)
    return []

def save_expense(expenses):
    with open(data_file, "w") as f:
        json.dump(expenses, f, indent=2)


# helper
def separator(title = ""):
    width = 52
    if title:
        print(f"\n{'-' * 5} {title} {'-' *(width - len(title)-7)}")
    else:
        print("-" * width)

def get_float(prompt, min_value = 0):
    while True:
        try:
            value = float(input(prompt))
            if value < min_value:
                print(f"value must be greater than {min_value}")
            else :
                return value
        except ValueError:
            print("Enter a valid number")

def get_int(prompt, min_value, max_value):
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            print(f"value must be between {min_value} and {max_value}")
        except ValueError:
            print("Enter a whole number")

def pick_category():
    print("\n CATEGORIES")
    for i, cat in enumerate(categories, 1):
        print(f"[{i: > 2}] {cat}")
    choice = get_int(" Pick a category (1-6): ",1, len(categories))
    return categories[choice - 1]

# features
def add_expense(expenses):
    separator(" Add expense ")
    description = input(" Description: ").strip()
    if not description:
        print(" Description cant be empty. ")
        return

    amount = get_float(f" Amount (R): ")
    category = pick_category()
    date = datetime.now().strftime("%d-%m-%Y")

    expense = {
        "date": date,
        "amount": amount,
        "category": category,
        "id": len(expenses) + 1,
        "description": description,
    }
    expenses.append(expense)
    save_expense(expenses)
    print(f"\n Added: {description} - R{amount:.2f} [{category}] 0n {date}")

def view_expenses(expenses):
    separator(" View expenses ")
    if not expenses:
        print(" No expenses recorded yet. ")
        return

    print(f" {'ID': < 5 } {'Date': < 12 } {'Category': < 14 } {'Amount': > 10} Description " )
    separator()
    for e in expenses:
        print(f" {e['id']: < 5 } {e['date']: < 12 } {e['category']: < 14 } R{e['amount']: > 10.2f} {e['description']}" "")

    separator()
    total_sum= sum(e['amount'] for e in expenses)
    print(f" {'Total expenses': < 32} {total_sum: > 10.2f}")

def delete_expense(expenses):
    separator(" Delete expense ")
    if not expenses:
        print(" No expenses recorded yet. ")
        return

    view_expenses(expenses)
    exp_id = get_int("\n Enter ID to delete(0 to cancel): ",0, max(e['id'] for e in expenses))
    if exp_id == 0:
        return

    match = next((e for e in expenses if e['id'] == exp_id), None)
    if not match:
        print(" ID not found.")
        return

    expenses.remove(match)
    save_expense(expenses)
    print(f" Deleted: {match('description')}")

def monthly_summary(expenses):
    global items
    separator(" Monthly summary ")
    if not expenses:
        print(" No expenses recorded yet. ")
        return

    months = {}
    for e in expenses:
        month =e['date': 7]
        months.setdefault(month, []).append(e)

    for month,items in sorted(months.items(), reverse=True):
        total = sum(i ('amount') for i in items )
        label = datetime.strptime(month, "%Y - %m").strftime("%B - %Y")
        print(f"\n {label} - R{total:.2f} ({len(items)} expenses)")
        separator()

    cats = {}
    for i in items:
        cats.setdefault(i['category'],0 )
        cats[ i['category'] ] += i['amount']

    for cat, amt in sorted(cats.items(), key=lambda x: -x[1]):
        bar_len = int((amt / total) * 20 )
        bar = bar_len + (20 - bar_len)
        print(f"{cat: < 14} {bar} R{amt: > 10.2f} ({amt / total * 100:.0f}%)")

def insights(expenses):
    separator(" Spending Insights ")
    if not expenses:
        print(" No expenses recorded yet. ")
        return
    total = sum(e['amount'] for e in expenses)
    count = len(expenses)
    avg = total / count

    cats = {}
    for e in expenses:
        cats.setdefault(e["category"], 0)
        cats[e['category']] += e['amount']

    top_cat = max(cats, key = cats.get)
    biggest = max(expenses, key = lambda e:e['amount'])
    print(f"\n {'Total spent': < 28 } R{total: > 12.2f}")
    print(f" {'Number of expenses': < 28 } R{count: > 12.2f}")
    print(f" {'Average per spent': < 28 } R{avg: > 12.2f}")
    print(f" {'Biggest spent': < 28 } R{biggest: > 12.2f} ({biggest['description']})")
    print(f" {'Top spent': < 28 } {top_cat: > 13} (R{cats[top_cat]:.2f})")

    separator()
    print("\n Spending by category ")
    for cat, amt in sorted(cats.items(), key=lambda x: -x[1]):
        print(f" {cat: < 16} R{amt: > 10.2f} ({amt / total * 100:.1f}%)")

# main menu
def main():
    expenses= load_expense()

    print("\n "+ "=" * 52)
    print("           EXPENSE TRACKER ")
    print("=" * 52)

    menu = {
        "1": ("Add expense", lambda: add_expense(expenses)),
        "2": ("View expenses", lambda: view_expenses(expenses)),
        "3": ("Delete expense", lambda: delete_expense(expenses)),
        "4": ("Monthly summary", lambda: monthly_summary(expenses)),
        "5": ("Insights", lambda: insights(expenses)),
        "6": ("Exit", None)
    }

    while True:
        print("\n What would you like to do?")
        for key, (label, _) in menu.items():
            print(f" [{key}] {label}")
        choice = input("\n Enter an option(1-6): ").strip()
        if choice == "6":
            print("\n Exiting...")
            break
        elif choice == "1":
            menu[choice][1]()
        else:
            print("\n Invalid option. Try again(1-6).")

if __name__ == "__main__":
    main()
