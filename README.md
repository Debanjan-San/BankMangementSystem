# 💳 Bank Management System

A command-line-based Bank Management System that allows users to securely manage bank accounts and transactions. Built with modularity and user experience in mind, featuring input validation, secure password entry, and transaction history tracking.

## ✨ Features

- 🏦 **Account Management**: Create, edit, and manage bank accounts.
- 💰 **Transactions**: Handle deposits, withdrawals, and transfers between accounts.
- 📜 **Transaction History**: View a detailed transaction log for each account.
- 🔒 **Secure Authentication**: Password and account number validation with retry attempts.
- ✅ **Input Validation**: Ensures correct entry for account numbers, passwords, and amounts.
- 🎨 **User-Friendly Interface**: Secure password input with color-coded terminal output for a smooth experience.

## 🛠️ How It Works

1. **Account Creation**: Set up a new account by providing user details, an initial deposit, and a password.
2. **Transactions**: Perform deposits, withdrawals, or transfers between accounts.
3. **Transaction History**: Retrieve a detailed history of all transactions related to an account.
4. **Security**: Secure password entry with multiple attempts allowed for account number and password validation.

### 📁 Files

- **`main.py`**: The main script that handles user input and navigation.
- **`account_manager.py`**: Manages account operations, including creation, deposits, withdrawals, and transfers.
- **`database/`**: Contains logic for data storage and retrieval.
  - **`database.py`**: Manages account data storage in JSON format.
  - **`model.py`**: Defines data models.
  - **`schema.py`**: Manages data schemas for accounts.

## 🖥️ Tech Stack

- **Language**: Python 🐍
- **External Libraries**:
  - `colorama` 🎨 (for color-coded terminal output)
- **Database**: JSON 📁 (used for data storage)

## 🚀 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/BankManagementSystem.git
   ```

2. Navigate to the project directory:

   ```bash
   cd BankManagementSystem
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python main.py
   ```

## 📚 How to Use

- **Create an Account**: Follow the prompts to set up an account with a name, deposit, and password.
- **Manage Transactions**: Use the menu to deposit, withdraw, or transfer funds.
- **View Details**: Check your account balance and transaction history via the menu.

## 🤝 Contribution

We welcome contributions! Here's how you can contribute:

1. Fork the repository 🍴.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request 🔄.

## 📜 License

This project is licensed under the MIT License.