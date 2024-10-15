import random
import string
from datetime import datetime

from database import Database, Model, Schema


class AccountManager:
    def __init__(self):
        user_schema = Schema(
            account_created_at=str,
            credits=int,
            name=str,
            account_number=str,
            password=str,
            age=int,
            birth_date=str,
            phone_number=str,
            transaction_history=list,
        )
        self.user_model = Model(
            collection_name="users", schema=user_schema, db_instance=Database()
        )

    # Function to add credits
    def add_credits(self, account_number, amount):
        user = self.user_model.find_one({"account_number": account_number})
        if user:
            new_credits = user["credits"] + amount
            self.user_model.update(
                {"account_number": account_number}, {"credits": new_credits}
            )
            return new_credits
        return None

    # Function to generate password
    def generate_password(self):
        characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        password = "".join(random.choice(characters) for _ in range(5))
        return password

    # Function to subtract credits
    def subtract_credits(self, account_number, amount):
        user = self.user_model.find_one({"account_number": account_number})
        if user and user["credits"] >= amount:
            new_credits = user["credits"] - amount
            self.user_model.update(
                {"account_number": account_number}, {"credits": new_credits}
            )
            return new_credits
        return None

    def create_account(self, name, age, birth_date, phone_number, credits=0):
        account_number = str(random.randint(10**12, 10**13 - 1))
        account_data = {
            "account_created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "credits": credits,
            "name": name,
            "account_number": account_number,
            "age": age,
            "password": self.generate_password(),
            "birth_date": birth_date,
            "phone_number": phone_number,
            "transaction_history": [],
        }
        new_account = self.user_model.create(account_data)
        return new_account

    def deposit(self, account_number, amount):
        new_credits = self.add_credits(account_number, amount)
        if new_credits is not None:
            user = self.user_model.find_one({"account_number": account_number})
            self._add_transaction(user, "deposit", amount)
            return f"Deposited {amount} to account {account_number}. New balance: {new_credits}."
        return "Account not found."

    def withdraw(self, account_number, amount):
        new_credits = self.subtract_credits(account_number, amount)
        if new_credits is not None:
            user = self.user_model.find_one({"account_number": account_number})
            self._add_transaction(user, "withdraw", amount)
            return f"Withdrew {amount} from account {account_number}. New balance: {new_credits}."
        return "Insufficient credits or account not found."

    def transfer_credits(self, sender_account_number, recipient_account_number, amount):
        sender_credits = self.subtract_credits(sender_account_number, amount)
        if sender_credits is not None:
            recipient_credits = self.add_credits(recipient_account_number, amount)
            if recipient_credits is not None:
                sender = self.user_model.find_one(
                    {"account_number": sender_account_number}
                )
                recipient = self.user_model.find_one(
                    {"account_number": recipient_account_number}
                )

                self._add_transaction(
                    sender, "transfer", amount, recipient_account_number
                )
                self._add_transaction(
                    recipient, "received", amount, sender_account_number
                )

                return f"Transferred {amount} from {sender_account_number} to {recipient_account_number}. New sender balance: {sender_credits}."
        return "Transfer failed: insufficient funds or account not found."

    def account_details(self, account_number):
        user = self.user_model.find_one({"account_number": account_number})
        if user:
            return {
                "name": user["name"],
                "age": user["age"],
                "birth_date": user["birth_date"],
                "phone_number": user["phone_number"],
                "credits": user["credits"],
                "account_number": user["account_number"],
            }
        return "Account not found."

    def get_transaction_history(self, account_number):
        user = self.user_model.find_one({"account_number": account_number})
        if user:
            return user["transaction_history"]
        return "Account not found."

    def check_password(self, account_number, entered_password):
        account = self.user_model.find_one({"account_number": account_number})
        if account:
            return account.get("password") == entered_password
        return False

    def check_account_number(self, account_number):
        account = self.user_model.find_one({"account_number": account_number})
        if not account:
            return False
        return True

    def edit_account_details(self, account_number, new_details):
        user = self.user_model.find_one({"account_number": account_number})
        if user:
            self.user_model.update({"account_number": account_number}, new_details)
            return "Account details updated."
        return "Account not found."

    # New function to get balance
    def get_balance(self, account_number):
        user = self.user_model.find_one({"account_number": account_number})
        if user:
            return user["credits"]
        return None  # or raise an exception if preferred

    # Private method to add transactions
    def _add_transaction(self, user, trans_type, amount, recipient_account_number=None):
        transaction = {
            "type": trans_type,
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        if recipient_account_number:
            transaction["recipient"] = recipient_account_number

        updated_history = user["transaction_history"] + [transaction]
        self.user_model.update(
            {"account_number": user["account_number"]},
            {"transaction_history": updated_history},
        )
