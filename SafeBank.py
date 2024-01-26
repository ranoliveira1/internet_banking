# This programa is a simple internet banking system, that provides basic services normally used, like balance check, transfering,
# withdrawing and depositing. All the functions are in a separate file "safebank_functions.py" and there is a single function
# for each banking operation.
# The client data is stored in a JSON file (clients.json), where there are all their data, like, sort-code, name, account number,
# password.
# The movements are stored in a JSON file (movements.json). Each operacion creates a new line in this file.

import json
import pandas as pd
from safebank_functions import *

class Client:
    def __init__(self, sort_code, account_number, password, name, email, phone, status):
        self.code = sort_code, ".", account_number
        self.sort_code = sort_code
        self.account_number = account_number
        self.password = password
        self.name = name
        self.email = email
        self.phone = phone
        self.status = status
    
    def __str__(self):
        return f"""
            Client: {self.name}
            """


class Movement:
    def __init__(self, client_code, date, value, nature, current_balance):
        self.client_code = client_code
        self.date = date
        self.value = value
        self.nature = nature
        self.current_balance = current_balance
        

# Load Clients and Movements file
client_file_source = "clients.json"
with open(client_file_source) as clients_json_file:
    clients_source = json.load(clients_json_file)

movement_file_source = "movements.json"
with open(movement_file_source) as movements_json_file:
    movements_source = json.load(movements_json_file)

clients = pd.DataFrame(clients_source)
clients.set_index("code", inplace=True)

movements = pd.DataFrame(movements_source)
movements.set_index("client_code", inplace=True)
#

# Menu
menu = f"""
{"*"*9} MENU {"*"*9}
1 - Checking Balances
2 - Transferring Funds
3 - Depositing Money
4 - Withdrawing Money
{"*"*24}
"""
#

# Header
print(
f"""
{"="*100}
{'SAFE BANK'.center(100)}
{'Welcome to your Internet Banking, 24hs available to you!'.center(100)}
{"="*100}
"""
)
#

# Ask user to login, requiring user and password
login_return = login(clients)
print()

if login_return != "exit":
    "Personalized Greetings"
    print(f"Welcome {clients.loc[login_return].client_name}!")
    print(menu)
    
    while True:
        # Ask user select an option based on the menu privously displayed
        option = input("Please, select an option (1/2/3/4) or 'exit' to quit: ")

        if option.lower() == "exit":
            break

        elif option not in ("1", "2", "3", "4"):
            print("Invalid option.\n")
        
        elif option == "1":  #Checking Balances
            balance(movements, login_return)

        elif option == "2":  #Transferring Funds
            transaction = transfer(movements, login_return, movement_file_source)
            
            if transaction:
                # As the function updates the file, now the program opens it again.
                with open(movement_file_source) as movements_json_file:
                    movements_source = json.load(movements_json_file)

                movements = pd.DataFrame(movements_source)
                movements.set_index("client_code", inplace=True)

                print("Successul Transfer.\n")

        elif option == "3":  #Depositing Money
            transaction = deposit(movements, login_return, movement_file_source)
            
            if transaction:
                # As the function updates the file, now the program opens it again.
                with open(movement_file_source) as movements_json_file:
                    movements_source = json.load(movements_json_file)

                movements = pd.DataFrame(movements_source)
                movements.set_index("client_code", inplace=True)

                print("Successul Deposit.\n")
        
        elif option == "4":  # Withdrawing Money
            transaction = withdraw(movements, login_return, movement_file_source)
            
            if transaction:
                # As the function updates the file, now the program opens it again.
                with open(movement_file_source) as movements_json_file:
                    movements_source = json.load(movements_json_file)

                movements = pd.DataFrame(movements_source)
                movements.set_index("client_code", inplace=True)

                print("Successul Transfer.\n")


print("\nThank you for using our Internet Banking!\n")

