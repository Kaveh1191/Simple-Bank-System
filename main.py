import sys
import json
import os
from datetime import datetime

Data = "accounts.json"

class BankAccount:
    def __init__(self, owner, password):
        self.__balance = 0
        self.__owner = owner
        self.__password = password
        self.__authentication = False
        self.__history = []

    def transaction(self):
        if self.__authentication:
            if not self.__history:
                print("No transactions yet!!!")
            else:
                print("Transactions list: ")
                for item in self.__history:
                    print(item)
        else:
            print("Access denied. please authenticate first.")

    def authenticate(self, password):
        if password == self.__password:
            self.__authentication = True
            print("Authenticated")
            return True
        else:
            print("Wrong password")
            return False

    def deposit(self, amount):
        self.__balance += amount
        transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__history.append(f"[{transaction_time}] Deposit ${amount}")
        print(f"${amount} has been deposited.")

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
            transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.__history.append(f"[{transaction_time}] Withdrew ${amount}")
        else:
            print("Not enough funds")

    def display_info(self):
        if self.__authentication:
            print(f"owner of account {self.__owner} and balance ${self.__balance}")
        else:
            print("Access denied. Please authenticate first.")

    def change_password(self, password, new_password):
        if password == self.__password:
            self.__password = new_password
            self.__authentication = False
            print("Password changed. Please login again")
        else:
            sys.exit('Passwords do not match')

    def to_dict(self):
        return {
            "owner": self.__owner,
            "balance": self.__balance,
            "history": self.__history,
            "password": self.__password
        }

    def load_data(self, data):
        self.__balance = data.get("balance", 0)
        self.__history = data.get("history", [])

def save_accounts(accounts):
    data = {username: account.to_dict() for username, account in accounts.items()}
    with open(Data, "w") as file:
        json.dump(data, file, indent=4)

def load_accounts():
    if not os.path.exists(Data):
        return {}
    with open(Data, "r") as file:
        try:
            raw_data = json.load(file)
        except json.JSONDecodeError:
            return {}
    accounts = {}
    for username, data in raw_data.items():
        account = BankAccount(data["owner"], data["password"])
        account.load_data(data)
        accounts[username] = account
    return accounts

class BankApp:
    def __init__(self, account, accounts, username):
        self.account = account
        self.accounts = accounts
        self.username = username
        self.max_try = 3

    def run(self):
        for attempt in range(self.max_try):
            pass_check = input("Enter your password: ")
            if self.account.authenticate(pass_check):
                break
            else:
                print(f"Attempt {attempt + 1} of {self.max_try} failed")
        else:
            sys.exit("Too many incorrect password.")

        while True:
            print(" Bank Menu ")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Display Account Information")
            print("4. Change Password")
            print("5. Transactions")
            print("6. Exit")

            user_input = input("Enter your choice: ")

            if user_input == "1":
                amount = int(input("Enter amount to deposit: "))
                self.account.deposit(amount)

            elif user_input == "2":
                amount = int(input("Enter amount to withdraw: "))
                self.account.withdraw(amount)

            elif user_input == "3":
                self.account.display_info()

            elif user_input == "4":
                old_pass = input("Enter your current password: ")
                if self.account.authenticate(old_pass):
                    while True:
                        new_pass = input("Enter your new password: ")
                        if new_pass.strip() == "":
                            print("new password cannot be empty")
                        else:
                            break
                    for attempt in range(self.max_try):
                        confirm = input("Please re-enter your new password: ")
                        if confirm == new_pass:
                            self.account.change_password(old_pass, new_pass)
                            print("Password changed")
                            break
                        else:
                            print(f"Attempts {attempt + 1} of {self.max_try} failed.The new password do not match.")
                            if attempt == self.max_try - 1:
                                sys.exit("Too many incorrect password.")
                    for attempt in range(self.max_try):
                        re_login = input("Please re-enter your new password: ")
                        if self.account.authenticate(re_login):
                            break
                        else:
                            print(f"Attempts {attempt + 1} of {self.max_try} failed.")
                    else:
                        sys.exit("Too many incorrect password.")
                else:
                    print("Wrong password. could not change password.")


            elif user_input == "5":
                self.account.transaction()

            elif user_input == "6":
                self.accounts[self.username] = self.account
                save_accounts(self.accounts)
                sys.exit("GoodBye")

            else:
                print("Invalid Input")

            self.accounts[self.username] = self.account
            save_accounts(self.accounts)

def main():
    accounts = load_accounts()

    while True:
        print("Bank System")
        print("1.Sign Up")
        print("2.Login")
        print("3.Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user_name = input("Enter your username: ")
            if user_name in accounts:
                print("Account already exists")
                continue
            else:
                password = input("Enter your password: ")
                accounts[user_name] = BankAccount(user_name, password)
                print("Account created")

        elif choice == "2":
            user_name = input("Enter your username: ")
            if user_name not in accounts:
                print("Account does not exist")
                continue
            else:
                app = BankApp(accounts[user_name], accounts, user_name)
                app.run()

        elif choice == "3":
            print("Have a good time.")
            save_accounts(accounts)
            break

        else:
            print("Invalid Input")

if __name__ == "__main__":
    main()


