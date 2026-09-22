"""

Banking System Mini Project
A beginner-friendly, menu-driven command-line banking application.

Features:
1. Create Account (with unique 8-digit account number and validation)
2. Login (with account number and 4-digit PIN)
3. Check Balance
4. Deposit Money
5. Withdraw Money
6. Transfer Money (between two accounts with history updated for both)
7. Transaction History
8. Change PIN
9. Logout & Exit
10. Data Persistence via JSON file

Concepts Used:
- Variables & Data Types (strings, integers, floats, booleans)
- Conditionals (if, elif, else)
- Loops (while, for)
- Functions
- Dictionaries & Lists
- String Operations (.strip(), .isdigit(), formatting)
- Basic Exception Handling (try / except)
- File Handling (json read/write)
- Standard Modules (json, os, random, datetime)

"""

import os
import json
import random
import datetime

# Name of the file where account data is saved
DATA_FILE = "accounts.json"


# FILE HANDLING FUNCTIONS

def load_accounts():
    """
    Load account data from the JSON file if it exists.
    Returns an empty dictionary if the file does not exist or cannot be read.
    """
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r") as file:
            accounts = json.load(file)
            return accounts
    except (json.JSONDecodeError, OSError):
        print("\n[Warning] Could not read accounts.json. Starting with empty data.")
        return {}


def save_accounts(accounts):
    """
    Save the current accounts dictionary into the JSON file.
    """
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(accounts, file, indent=4)
    except OSError as e:
        print(f"\n[Error] Failed to save account data to file: {e}")



# HELPER FUNCTIONS

def get_current_date_and_time():
    """
    Return current date and time as formatted strings:
    Date format: DD-MM-YYYY
    Time format: HH:MM AM/PM
    """
    now = datetime.datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    time_str = now.strftime("%I:%M %p")
    return date_str, time_str


def generate_account_number(accounts):
    """
    Generate a unique 8-digit bank account number using random.randint.
    Ensures the generated account number does not already exist in accounts.
    """
    while True:
        # Generate an 8-digit random integer and convert it to string
        acc_num = str(random.randint(10000000, 99999999))
        if acc_num not in accounts:
            return acc_num


def add_transaction(account, transaction_type, amount, balance_after, sender=None, receiver=None):
    """
    Create a transaction record dictionary and append it to the account's transaction list.
    """
    date_str, time_str = get_current_date_and_time()

    record = {
        "type": transaction_type,
        "amount": amount,
        "date": date_str,
        "time": time_str,
        "balance": balance_after
    }

    if sender:
        record["sender"] = sender
    if receiver:
        record["receiver"] = receiver

    account["transactions"].append(record)



# FEATURE 1: CREATE ACCOUNT

def create_account(accounts):
    """
    Prompt user for account details, validate inputs, generate a unique account
    number, initialize starting balance to ₹0, and save the account.
    """
    print("\n---------------------------------")
    print("CREATE NEW ACCOUNT")
    print("---------------------------------")

    # 1. Full Name validation
    name = input("Enter Full Name: ").strip()
    if name == "":
        print("\n[Error] Name cannot be empty.")
        return

    # 2. Phone Number validation
    phone = input("Enter Phone Number: ").strip()
    if not phone.isdigit():
        print("\n[Error] Phone number should contain only digits.")
        return

    # 3. PIN validation
    pin = input("Create a 4-digit PIN: ").strip()
    if not (pin.isdigit() and len(pin) == 4):
        print("\n[Error] PIN must contain exactly 4 digits.")
        return

    # 4. Confirm PIN validation
    confirm_pin = input("Confirm PIN: ").strip()
    if pin != confirm_pin:
        print("\n[Error] PIN and Confirm PIN do not match.")
        return

    # Generate unique account number
    account_number = generate_account_number(accounts)

    # Store account information in the accounts dictionary
    # Note: In a real-world production system, credentials/PINs would be
    # securely hashed with cryptographic algorithms (e.g. bcrypt/argon2).
    # For this student assignment, we store it directly.
    accounts[account_number] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": 0.0,
        "transactions": []
    }

    # Save to file
    save_accounts(accounts)

    print("\nAccount created successfully!")
    print(f"Account Holder: {name}")
    print(f"Account Number: {account_number}")
    print("Please safely remember your Account Number and PIN to login!")


# FEATURE 2: LOGIN

def login(accounts):
    """
    Prompt user for account number and PIN.
    If valid, open the account dashboard menu.
    """
    print("\n---------------------------------")
    print("ACCOUNT LOGIN")
    print("---------------------------------")

    account_number = input("Enter Account Number: ").strip()
    pin = input("Enter PIN: ").strip()

    # Verify if account exists and PIN matches
    if account_number in accounts and accounts[account_number]["pin"] == pin:
        customer_name = accounts[account_number]["name"]
        print("\nLogin Successful!")
        print(f"Welcome, {customer_name}")

        # Open Account Dashboard
        account_menu(account_number, accounts)
    else:
        print("\nInvalid Account Number or PIN.")


# FEATURE 3: CHECK BALANCE

def check_balance(account_number, accounts):
    """
    Display account holder name, account number, and current balance.
    """
    account = accounts[account_number]
    print("\n---------------------------------")
    print("BALANCE DETAILS")
    print("---------------------------------")
    print(f"Account Holder : {account['name']}")
    print(f"Account Number : {account_number}")
    print(f"Current Balance: ₹{account['balance']:,.2f}")


# FEATURE 4: DEPOSIT MONEY

def deposit_money(account_number, accounts):
    """
    Deposit money into the current account, update balance,
    record transaction, and save data.
    """
    print("\n---------------------------------")
    print("DEPOSIT MONEY")
    print("---------------------------------")

    amount_input = input("Enter amount to deposit: ").strip()

    # Validate numeric value using try/except
    try:
        amount = float(amount_input)
    except ValueError:
        print("\n[Error] Invalid input. Amount must be a valid number.")
        return

    # Validate amount > 0
    if amount <= 0:
        print("\n[Error] Deposit amount must be greater than 0.")
        return

    account = accounts[account_number]
    account["balance"] += amount

    # Record the transaction
    add_transaction(
        account=account,
        transaction_type="Deposit",
        amount=amount,
        balance_after=account["balance"]
    )

    # Save changes to file
    save_accounts(accounts)

    print("\nDeposit Successful!")
    print(f"Deposited      : ₹{amount:,.2f}")
    print(f"Current Balance: ₹{account['balance']:,.2f}")



# FEATURE 5: WITHDRAW MONEY


def withdraw_money(account_number, accounts):
    """
    Withdraw money from the account if balance is sufficient,
    record transaction, and save data.
    """
    print("\n---------------------------------")
    print("WITHDRAW MONEY")
    print("---------------------------------")

    amount_input = input("Enter amount to withdraw: ").strip()

    # Validate numeric value
    try:
        amount = float(amount_input)
    except ValueError:
        print("\n[Error] Invalid input. Amount must be a valid number.")
        return

    # Validate amount > 0
    if amount <= 0:
        print("\n[Error] Withdrawal amount must be greater than 0.")
        return

    account = accounts[account_number]

    # Validate sufficient balance
    if amount > account["balance"]:
        print("\nInsufficient Balance.")
        return

    # Deduct amount
    account["balance"] -= amount

    # Record transaction
    add_transaction(
        account=account,
        transaction_type="Withdrawal",
        amount=amount,
        balance_after=account["balance"]
    )

    # Save changes to file
    save_accounts(accounts)

    print("\nWithdrawal Successful!")
    print(f"Withdrawn      : ₹{amount:,.2f}")
    print(f"Current Balance: ₹{account['balance']:,.2f}")


# FEATURE 6: TRANSFER MONEY


def transfer_money(account_number, accounts):
    """
    Transfer money from sender account to receiver account.
    Validations:
    1. Receiver account must exist.
    2. Cannot transfer to own account.
    3. Amount must be greater than 0.
    4. Sender must have sufficient balance.
    Updates balances and transaction histories for both users.
    """
    print("\n---------------------------------")
    print("TRANSFER MONEY")
    print("---------------------------------")

    receiver_acc = input("Enter Receiver Account Number: ").strip()

    # 1. Receiver must exist
    if receiver_acc not in accounts:
        print("\n[Error] Receiver account does not exist.")
        return

    # 2. Cannot transfer to own account
    if receiver_acc == account_number:
        print("\n[Error] You cannot transfer money to your own account.")
        return

    amount_input = input("Enter Amount: ").strip()

    # Validate numeric value
    try:
        amount = float(amount_input)
    except ValueError:
        print("\n[Error] Invalid input. Amount must be a valid number.")
        return

    # 3. Amount must be greater than 0
    if amount <= 0:
        print("\n[Error] Transfer amount must be greater than 0.")
        return

    sender_account = accounts[account_number]
    receiver_account = accounts[receiver_acc]

    # 4. Sender must have sufficient balance
    if amount > sender_account["balance"]:
        print("\n[Error] Insufficient Balance for transfer.")
        return

    # Deduct from sender, add to receiver
    sender_account["balance"] -= amount
    receiver_account["balance"] += amount

    # Record transaction for sender
    add_transaction(
        account=sender_account,
        transaction_type="Transfer Sent",
        amount=amount,
        balance_after=sender_account["balance"],
        receiver=receiver_acc
    )

    # Record transaction for receiver
    add_transaction(
        account=receiver_account,
        transaction_type="Transfer Received",
        amount=amount,
        balance_after=receiver_account["balance"],
        sender=account_number
    )

    # Save updated data for both accounts
    save_accounts(accounts)

    print("\nTransfer Successful!")
    print(f"Transferred      : ₹{amount:,.2f}")
    print(f"To               : {receiver_acc}")
    print(f"Remaining Balance: ₹{sender_account['balance']:,.2f}")



# FEATURE 7: TRANSACTION HISTORY


def transaction_history(account_number, accounts):
    """
    Display all transactions performed by the logged-in user.
    """
    account = accounts[account_number]
    transactions = account.get("transactions", [])

    print("\n=========================================")
    print("TRANSACTION HISTORY")
    print("=========================================")

    if not transactions:
        print("No transactions found.")
        return

    for index, tx in enumerate(transactions, start=1):
        print(f"\n{index}.")
        print(f"Type   : {tx.get('type')}")
        print(f"Amount : ₹{tx.get('amount', 0.0):,.2f}")

        # Show receiver if transfer was sent
        if "receiver" in tx:
            print(f"Receiver: {tx.get('receiver')}")

        # Show sender if transfer was received
        if "sender" in tx:
            print(f"Sender  : {tx.get('sender')}")

        print(f"Date   : {tx.get('date')}")
        print(f"Time   : {tx.get('time')}")
        print(f"Balance: ₹{tx.get('balance', 0.0):,.2f}")

        if index < len(transactions):
            print("---")


# FEATURE 8: CHANGE PIN


def change_pin(account_number, accounts):
    """
    Allow user to change their 4-digit PIN after verifying current PIN.
    """
    print("\n---------------------------------")
    print("CHANGE PIN")
    print("---------------------------------")

    account = accounts[account_number]

    current_pin = input("Enter Current PIN: ").strip()

    # Verify current PIN
    if current_pin != account["pin"]:
        print("\n[Error] Current PIN is incorrect.")
        return

    new_pin = input("Enter New 4-digit PIN: ").strip()

    # Validate new PIN format (numeric and exactly 4 digits)
    if not (new_pin.isdigit() and len(new_pin) == 4):
        print("\n[Error] New PIN must contain exactly 4 digits.")
        return

    confirm_new_pin = input("Confirm New PIN: ").strip()

    # Verify confirmation match
    if new_pin != confirm_new_pin:
        print("\n[Error] New PIN and Confirm New PIN do not match.")
        return

    # Update PIN
    account["pin"] = new_pin

    # Save to file
    save_accounts(accounts)

    print("\nPIN changed successfully.")



# ACCOUNT DASHBOARD (LOGGED-IN MENU)


def account_menu(account_number, accounts):
    """
    Keep displaying the account dashboard menu until the user selects Logout (Option 7).
    """
    while True:
        print("\n=================================")
        print("ACCOUNT MENU")
        print("============")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Logout")
        print("=================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            check_balance(account_number, accounts)
        elif choice == "2":
            deposit_money(account_number, accounts)
        elif choice == "3":
            withdraw_money(account_number, accounts)
        elif choice == "4":
            transfer_money(account_number, accounts)
        elif choice == "5":
            transaction_history(account_number, accounts)
        elif choice == "6":
            change_pin(account_number, accounts)
        elif choice == "7":
            print("\nLogged out successfully.")
            break
        else:
            print("\n[Invalid Choice] Please select a number from 1 to 7.")



# MAIN MENU & ENTRY POINT


def main():
    """
    Main entry point for the Banking System application.
    Loads existing accounts, presents the main menu, and handles top-level actions.
    """
    # Load existing account data from JSON file
    accounts = load_accounts()

    while True:
        print("\n=================================")
        print("BANKING SYSTEM")
        print("==============")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        print("=================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_account(accounts)
        elif choice == "2":
            login(accounts)
        elif choice == "3":
            print("\nThank you for using Banking System. Goodbye!\n")
            break
        else:
            print("\n[Invalid Choice] Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
