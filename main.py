import random
import re
from getpass import getpass

from colorama import Fore, Style, init

from account_manager import AccountManager

# Initialize colorama
init(autoreset=True)


class Menu:
    def __init__(self, account_manager):
        self.account_manager = account_manager

    def display(self):
        while True:
            print(Fore.CYAN + Style.BRIGHT + "\n=== Account Management System ===")
            print(Fore.GREEN + "1. Create Account")
            print(Fore.GREEN + "2. Deposit Money")
            print(Fore.GREEN + "3. Withdraw Money")
            print(Fore.GREEN + "4. Transfer Credits")
            print(Fore.GREEN + "5. Account Details")
            print(Fore.GREEN + "6. Show Transaction History")
            print(Fore.GREEN + "7. Edit Account Details")
            print(Fore.GREEN + "8. Check Balance")
            print(Fore.RED + "9. Exit")
            print(Style.RESET_ALL)

            choice = input(Fore.YELLOW + "Enter your choice (1-9): ")

            match choice:
                case "1":
                    self.create_account()
                case "2":
                    self.deposit_money()
                case "3":
                    self.withdraw_money()
                case "4":
                    self.transfer_credits()
                case "5":
                    self.account_details()
                case "6":
                    self.show_transaction_history()
                case "7":
                    self.edit_account_details()
                case "8":
                    self.check_balance()
                case "9":
                    print(Fore.RED + "Exiting the system. Goodbye!")
                    break
                case _:
                    print(Fore.RED + "Invalid choice. Please select a valid option.")

    def validate_account_number(self, account_number):
        return account_number.isdigit() and len(account_number) == 13

    def validate_amount(self, amount):
        try:
            amount = float(amount)
            return amount > 0
        except ValueError:
            return False

    def validate_password(self, password):
        return len(password) == 5 and all(char.isalnum() for char in password)

    def validate_date(self, date_str):
        pattern = r"^\d{4}-\d{2}-\d{2}$"  # YYYY-MM-DD format
        return re.match(pattern, date_str) is not None

    def create_account(self):
        for attempt in range(2):
            try:
                name = input(Fore.YELLOW + "Enter your name: ")
                age = int(input(Fore.YELLOW + "Enter your age: "))
                birth_date = input(Fore.YELLOW + "Enter your birth date (YYYY-MM-DD): ")
                if not self.validate_date(birth_date):
                    raise ValueError("Birth date must be in YYYY-MM-DD format.")
                phone_number = input(Fore.YELLOW + "Enter your phone number: ")

                # Check for empty or invalid inputs
                if not name or age <= 0 or not phone_number.isdigit():
                    raise ValueError("Invalid inputs. Please enter valid details.")

                credits = random.randint(10000, 99999)
                account = self.account_manager.create_account(
                    name, age, birth_date, phone_number, credits
                )
                print(
                    Fore.GREEN
                    + f"Account created successfully! \nAccount Number: {
                      account['account_number']}\nPassword: {account['password']}"
                )
                return  # Exit after successful account creation
            except ValueError as ve:
                print(Fore.RED + f"Error: {ve}")
                if attempt < 1:  # Only prompt again if this isn't the last attempt
                    print(Fore.YELLOW + "Please try again.")
            except Exception as e:
                print(Fore.RED + f"Unexpected error occurred: {e}")
                break  # Break on unexpected error

        print(Fore.RED + "Too many invalid attempts. Returning to menu.")

    def verify_password(self, account_number):
        for attempt in range(2):
            password = getpass(
                # Secure input
                Fore.YELLOW
                + "Enter your password (5 characters): "
            )
            if not self.validate_password(password):
                print(Fore.RED + "Password must be a 5 character alphanumeric string.")
                if attempt < 1:  # Only prompt again if this isn't the last attempt
                    print(Fore.YELLOW + "Please try again.")
            else:
                return self.account_manager.check_password(account_number, password)

        print(Fore.RED + "Too many invalid attempts. Returning to menu.")
        return False

    def verify_account(self):
        for attempt in range(2):
            account_number = input(Fore.YELLOW + "Enter account number (13 digits): ")

            # Validate if account number is 13 digits long and exists
            if not self.validate_account_number(account_number):
                print(Fore.RED + "Account number must be a 13-digit number.")
                if attempt < 1:  # Only prompt again if this isn't the last attempt
                    print(Fore.YELLOW + "Please try again.")
            elif not self.account_manager.check_account_number(account_number):
                print(Fore.RED + f"Account number {account_number} does not exist.")
                if attempt < 1:  # Only prompt again if this isn't the last attempt
                    print(Fore.YELLOW + "Please try again.")
            else:
                return account_number  # Return valid account number if all checks pass

        print(Fore.RED + "Too many invalid attempts. Returning to menu.")
        return None  # Return None if all attempts fail

    def deposit_money(self):
        for attempt in range(2):
            account_number = self.verify_account()  # Call the updated function
            if account_number is None:
                return

            amount = input(Fore.YELLOW + "Enter amount to deposit: ")
            if not self.validate_amount(amount):
                print(Fore.RED + "Invalid amount entered. Please enter a valid number.")
                if attempt < 1:  # Only prompt again if this isn't the last attempt
                    print(Fore.YELLOW + "Please try again.")
                continue

            amount = float(amount)  # Convert to float after validation

            # Verify password
            if not self.verify_password(account_number):
                print(Fore.RED + "Incorrect password. Operation denied.")
                return

            print(Fore.GREEN + self.account_manager.deposit(account_number, amount))
            return  # Exit after successful deposit

        print(Fore.RED + "Too many invalid attempts. Returning to menu.")

    def withdraw_money(self):
        for attempt in range(2):
            account_number = self.verify_account()  # Call the updated function
            if account_number is None:
                return

            amount = input(Fore.YELLOW + "Enter amount to withdraw: ")
            if not self.validate_amount(amount):
                print(Fore.RED + "Invalid amount entered. Please enter a valid number.")
                if attempt < 1:  # Only prompt again if this isn't the last attempt
                    print(Fore.YELLOW + "Please try again.")
                continue

            amount = float(amount)  # Convert to float after validation

            # Fetch the current balance
            current_balance = self.account_manager.get_balance(account_number)

            if amount > current_balance:
                print(
                    Fore.RED
                    + f"Insufficient balance. Your current balance is {current_balance}"
                )
                return

            # Verify password
            if not self.verify_password(account_number):
                print(Fore.RED + "Incorrect password. Operation denied.")
                return

            print(Fore.GREEN + self.account_manager.withdraw(account_number, amount))
            return  # Exit after successful withdrawal

        print(Fore.RED + "Too many invalid attempts. Returning to menu.")

    def transfer_credits(self):
        for attempt in range(2):
            sender_account = self.verify_account()  # Call the updated function
            if sender_account is None:
                return

            recipient_account = self.verify_account()  # Call the updated function
            if recipient_account is None:
                return

            amount = input(Fore.YELLOW + "Enter amount to transfer: ")
            if not self.validate_amount(amount):
                print(Fore.RED + "Invalid amount entered. Please enter a valid number.")
                if attempt < 1:  # Only prompt again if this isn't the last attempt
                    print(Fore.YELLOW + "Please try again.")
                continue

            amount = float(amount)  # Convert to float after validation

            # Verify sender's password
            if not self.verify_password(sender_account):
                print(Fore.RED + "Incorrect password. Operation denied.")
                return

            # Check if sender has enough credits
            sender_details = self.account_manager.account_details(sender_account)
            if sender_details["credits"] < amount:
                print(Fore.RED + "Insufficient credits. Transfer aborted.")
                return

            # Perform the transfer if all checks pass
            print(
                Fore.GREEN
                + self.account_manager.transfer_credits(
                    sender_account, recipient_account, amount
                )
            )
            return  # Exit after successful transfer

        print(Fore.RED + "Too many invalid attempts. Returning to menu.")

    def account_details(self):
        account_number = self.verify_account()  # Call the updated function
        if account_number is None:
            return

        # Verify password
        if not self.verify_password(account_number):
            print(Fore.RED + "Incorrect password. Operation denied.")
            return
        details = self.account_manager.account_details(account_number)
        if isinstance(details, dict):
            print(Fore.CYAN + Style.BRIGHT + "\n=== Account Details ===")
            print(
                Fore.MAGENTA
                + f"Name: {details['name']}\nAge: {details['age']}\nBirth_date: {details['birth_date']}\nPhone_number: {
                  details['phone_number']}\nCredits: {details['credits']}\nAccount_number: {details['account_number']}"
            )
        else:
            print(Fore.RED + details)
        return  # Exit after displaying account details

    def show_transaction_history(self):
        account_number = self.verify_account()  # Call the updated function
        if account_number is None:
            return

        # Verify password
        if not self.verify_password(account_number):
            print(Fore.RED + "Incorrect password. Operation denied.")
            return
        transactions = self.account_manager.get_transaction_history(account_number)
        if transactions:
            print(Fore.CYAN + Style.BRIGHT + "\n=== Transaction History ===")
            for trans in transactions:
                trans_type = trans["type"]
                amount = trans["amount"]
                date = trans["date"]
                print(Fore.MAGENTA + f"{trans_type:<10} {amount:<10} {date:<20}")
        else:
            print(Fore.RED + "No transactions found or account not found.")
        return

    def edit_account_details(self):
        for attempt in range(2):
            account_number = self.verify_account()  # Call the updated function
            if account_number is None:
                return

            new_details = {}
            if (
                input(Fore.YELLOW + "Do you want to edit the name? (y/n): ").lower()
                == "y"
            ):
                new_details["name"] = input(Fore.YELLOW + "Enter new name: ")
            if (
                input(Fore.YELLOW + "Do you want to edit the age? (y/n): ").lower()
                == "y"
            ):
                new_age = input(Fore.YELLOW + "Enter new age: ")
                if new_age.isdigit() and int(new_age) > 0:
                    new_details["age"] = int(new_age)
                else:
                    if attempt < 1:
                        print(Fore.RED + "Invalid age input.")
                    continue

            if (
                input(
                    Fore.YELLOW + "Do you want to edit the phone number? (y/n): "
                ).lower()
                == "y"
            ):
                new_details["phone_number"] = input(
                    Fore.YELLOW + "Enter new phone number: "
                )

            # Verify password
            if not self.verify_password(account_number):
                print(Fore.RED + "Incorrect password. Operation denied.")
                return

            # Update account details
            self.account_manager.edit_account_details(account_number, new_details)
            print(Fore.GREEN + "Account details updated successfully.")
            return  # Exit after updating account details

        print(Fore.RED + "Too many invalid attempts. Returning to menu.")

    def check_balance(self):
        account_number = self.verify_account()  # Call the updated function
        if account_number is None:
            return

        # Verify password
        if not self.verify_password(account_number):
            print(Fore.RED + "Incorrect password. Operation denied.")
            return
        balance = self.account_manager.get_balance(account_number)
        if balance is not None:
            print(Fore.GREEN + f"Current balance: {balance}")
        else:
            print(Fore.RED + "Account not found.")
        return


if __name__ == "__main__":
    account_manager = AccountManager()
    menu = Menu(account_manager)
    menu.display()
