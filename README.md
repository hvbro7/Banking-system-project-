# Banking System Mini Project

## Project Overview

The **Banking System Mini Project** is a beginner-friendly, menu-driven command-line banking application developed in Python. It allows users to register bank accounts, securely log in with a 4-digit PIN, deposit and withdraw funds, transfer money between accounts, view transaction histories, and update their credentials.

All account details and transactions are persisted locally using a structured JSON file (`accounts.json`), ensuring account balances and history are preserved even after the application restarts. The codebase uses clean, functional Python constructs without object-oriented programming (OOP) or external database libraries, making it accessible for students who have studied Python up to the NumPy level.

---

## Features

* **Create Account**: Register with full name, phone number, and a 4-digit PIN. Automatically generates an 8-digit random unique account number with a ₹0 starting balance.
* **Login**: Secure login authentication using the unique account number and PIN.
* **Check Balance**: View current account holder name, account number, and formatted balance.
* **Deposit**: Deposit funds with real-time balance updates and input validation.
* **Withdraw**: Withdraw money with balance sufficiency checks to prevent overdrafts.
* **Transfer**: Transfer money between two existing bank accounts, simultaneously updating balances and transaction records for both sender and receiver.
* **Transaction History**: View a chronologically recorded list of all deposits, withdrawals, and transfers with dates and times.
* **Change PIN**: Update the 4-digit PIN after confirming current credentials.
* **Logout**: Safely log out of the active account dashboard and return to the main menu without terminating the program.

---

## Python Concepts Used

* **Variables and Data Types**: String, integer, float, boolean.
* **Conditional Statements**: `if`, `elif`, and `else` for input validation and menu routing.
* **Loops**: `while` loops for continuous menu navigation and `for` loops for iterating through transaction histories.
* **Functions**: Modular functions with clean parameters and return values.
* **Lists**: Dynamically ordered transaction histories stored inside account records.
* **Dictionaries**: Key-value data modeling for account profiles and transaction entries.
* **String Operations**: String formatting (`f-strings`), `.strip()`, `.isdigit()`, and comma-separated currency representation.
* **Basic Exception Handling**: `try` / `except` blocks for handling non-numeric user inputs (`ValueError`) and safe file I/O operations (`OSError`, `json.JSONDecodeError`).
* **File Handling**: Reading and writing structured JSON data (`json.load`, `json.dump`) using `with open(...)`.
* **Standard Modules**:
  * `random`: Generating unique 8-digit bank account numbers.
  * `datetime`: Capturing current timestamps for transaction records.
  * `json`: Managing file persistence.
  * `os`: Checking file existence.

---

## How to Run

### Prerequisites
* Python 3.x installed on your computer.

### Execution
Open your terminal or command prompt, navigate to the project directory, and execute:

```bash
python banking_system.py
```

*(On macOS/Linux systems where Python 3 is mapped to `python3`, use `python3 banking_system.py`)*

---

## Project Structure

### Application Flow

```
Create Account
      ↓
Account Number + PIN
      ↓
    Login
      ↓
Account Menu
      ↓
Banking Operations (Deposit / Withdraw / Transfer / History / PIN)
      ↓
   Logout
      ↓
  Main Menu
      ↓
    Exit
```

### File Organization

```
banking-system/
│
├── banking_system.py   # Core application source code
├── accounts.json       # JSON data file storing accounts and transaction history
└── README.md           # Project documentation and guide
```
