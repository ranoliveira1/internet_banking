def login(df):
    """
    This function require user_code and password and check them in a pandas DF. 
    This DF has user as index and a column called password.
    Parameters:
        df (dataframe): a dataframe with the clients data (user as index and a column called 'password').
    Returns:
        user or 'exit' (str).
    """
    
    # Ask user the login and check if it is in DF (clients)
    while True:
        user = input("Login (or 'exit' to quit): ").strip()
        
        if user.lower() == "exit":
            return "exit"

        elif user in df.index:
            break
        else:
            print("Login not found.\n")

    # Ask user the password and check if it matches the user password is in DF (clients)
    while True:
        password = input("Password (or 'exit' to quit): ").strip()
        
        if password == "exit":
            return "exit"
        
        elif password == df.loc[user].password:
            break
        else:
            print("Incorrect Password.\n")
    
    return user


def balance(df, user):
    """
    This function prints out the current balance of a certain user. 
    Parameters:
        df (dataframe): a dataframe with the clients movements (user_code as index).
        user (str): user_code to match the df index.
    Returns:
        current_balance (float): the latest balance of a certain user.
    """
    
    try:
        # Select the rows of user_code passed as parameter. Sort it based on date, to have the latest as first.
        # Use iloc to pull the first line and the value of "current_balance" column.
        # If the user provided is not found in movements DF, it displays they have no found.
        user_movements = df.loc[user]
        current_balance = user_movements.sort_values("date", ascending=False).iloc[0, 3]
        return print(f"\nYour current balance is £{round(current_balance, 2)}\n")

    except:
        return print("\nNo movements found.\n")


def transfer(df, user, df_source):
    from datetime import datetime
    import pandas as pd
    """
    This function asks user the sort-code and account that will receive the payment
    and the amount. It also creates a new line for the movements DF and change the current balance
    Parameters:
        dataframe (dataframe): a dataframe with the clients movements (user_code as index).
        user (str): user_code to match the df index.
        df_source (str): path with the dataframe source.
    Returns:
        boolean (bool): True if transaction completed and DF with updated with the new transaction data.
    """
    transaction = False

    try:
        # Select the rows of user_code passed as parameter. Sort it based on date, to have the latest as first.
        # Use iloc to pull the first line and the value of "current_balance" column.
        # If the user provided is not found in movements DF, it displays this option is anavailable because have no found.
        user_movements = df.loc[user]
        current_balance = user_movements.sort_values("date", ascending=False).iloc[0, 3]
        print(f"\nThis is your current balance: £{round(current_balance, 2)}\n")

        if current_balance <= 0:
            return print("\nOption not available. Insufficient funds.\n")  
        
        else:
            # Ask user to provide the Sort-Code of the destination.
            while True:
                sort_code = input("Destination Sort-Code: ")
                if sort_code.lower() == "exit":
                    return transaction
                
                elif len(sort_code) == 0:
                    print("Invalid Sort-Code.\n")
                
                else:
                    break
            
            # Ask user to provide the Account number of the destination.
            while True:
                account = input("Destination Account: ")
                if account.lower() == "exit":
                    return transaction
                
                elif len(account) == 0:
                    print("Invalid Account number.\n")
                
                else:
                    break

            # Ask user to provide the amount of money to transfer.
            while True:
                amount = input("Amount to transfer: ")
                if amount.lower() == "exit":
                    return transaction
                
                elif len(amount) == 0:
                    print("Invalid amount. Please enter a number.\n")

                else:
                    try:
                        # If the user doesn't provide a number or the found is not enough, they're asked to provide another number.
                        amount = float(amount)

                        if amount <= 0:
                            print("Please, enter a positive number.")

                        elif amount > current_balance:
                            print("Insufficient funds.\n")
                        
                        else:
                            break
                    
                    except:
                        print("Invalid amount. Please enter a number.\n")
            
            # Provide the user a summary of the transaction and ask confirmation.
            print(f"You are transfering £{amount} to Sort-Code {sort_code} Account {account}.\n")
            while True:
                confirmation = input("Confirm ('Yes' or 'No'): ")
                
                if confirmation.lower() in ("no", "exit"):
                    return transaction

                # Create a dictionary with the transaction information, apend it to the DF.
                elif confirmation.lower() == "yes":
                    try:
                        new = {
                        "client_code": user,
                        "date": [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                        "value": [amount],
                        "nature": ["Debit"],
                        "current_balance": [current_balance-amount]
                        }

                        df.reset_index(inplace=True)
                        df = pd.concat([df, pd.DataFrame(new)], axis=0)
                        df.reset_index(drop=True, inplace=True)
                        df.to_json(df_source, indent=4, orient="records")
                    
                        transaction = True
                    
                    except:
                        print("Error on transaction. Call your account manager.\n")
                        transaction = False
                        break
                    
                    return transaction

                else:
                    print("Invalid option.\n")

    except:
        return print("\nOption not available. Insufficient funds.\n")


def deposit(df, user, df_source):
    from datetime import datetime
    import pandas as pd
    """
    This function asks user the amount of money they wish to deposit.
    It also creates a new line for the movements DF and change the current balance
    Parameters:
        dataframe (dataframe): a dataframe with the clients movements (user_code as index).
        user (str): user_code to match the df index.
        df_source (str): path with the dataframe source.
    Returns:
        boolean (bool): True if transaction completed and DF with updated with the new transaction data.
    """
    transaction = False

    try:
        # Select the rows of user_code passed as parameter. Sort it based on date, to have the latest as first.
        # Use iloc to pull the first line and the value of "current_balance" column.
        # If the user provided is not found in movements DF, it displays this option is anavailable because have no found.
        user_movements = df.loc[user]
        current_balance = user_movements.sort_values("date", ascending=False).iloc[0, 3]

        while True:
            # Ask the user to provide the amount to deposit.
            amount = input("Please inform the amount to deposit: ")

            if amount.lower() == "exit":
                return transaction
            
            try:
                amount = float(amount)

                if amount <= 0:
                    print("Invalid amount. Please enter a positive number.\n")
                
                else:

                    try:
                        # Create a dictionary with the transaction information, apend it to the DF.
                        new = {
                        "client_code": user,
                        "date": [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                        "value": [amount],
                        "nature": ["Credit"],
                        "current_balance": [current_balance+amount]
                        }

                        df.reset_index(inplace=True)
                        df = pd.concat([df, pd.DataFrame(new)], axis=0)
                        df.reset_index(drop=True, inplace=True)
                        df.to_json(df_source, indent=4, orient="records")
                    
                        transaction = True
                    
                    except:
                        print("Error on transaction. Call your account manager.\n")
                        transaction = False
                        break
                    
                    return transaction
            
            except:
                print("Invalid amount. Please enter a number.\n")

    except:
        print("Error on transaction. Call your account manager.\n")
        return transaction
    

def withdraw(df, user, df_source):
    from datetime import datetime
    import pandas as pd
    """
    This function asks user the an amount to be withdrawed. 
    It also creates a new line for the movements DF and change the current balance
    Parameters:
        dataframe (dataframe): a dataframe with the clients movements (user_code as index).
        user (str): user_code to match the df index.
        df_source (str): path with the dataframe source.
    Returns:
        boolean (bool): True if transaction completed and DF with updated with the new transaction data.
    """
    transaction = False

    try:
        # Select the rows of user_code passed as parameter. Sort it based on date, to have the latest as first.
        # Use iloc to pull the first line and the value of "current_balance" column.
        # If the user provided is not found in movements DF, it displays this option is anavailable because have no found.
        user_movements = df.loc[user]
        current_balance = user_movements.sort_values("date", ascending=False).iloc[0, 3]
        print(f"\nThis is your current balance: £{round(current_balance, 2)}\n")

        if current_balance <= 0:
            return print("\nOption not available. Insufficient funds.\n")  
        
        else:
            # Ask user to provide the amount of money to withdraw.
            while True:
                amount = input("Amount to withdraw: ")
                if amount.lower() == "exit":
                    return transaction
                
                elif len(amount) == 0:
                    print("Invalid amount. Please enter a number.\n")
                
                else:
                    try:
                        # If the user doesn't provide a number or the found is not enough, they're asked to provide another number.
                        amount = float(amount)
                        if amount <= 0:
                            print("Please, enter a positive number.")                        
                        
                        elif amount > current_balance:
                            print("Insufficient funds.\n")
                        
                        else:
                            break
                    
                    except:
                        print("Invalid amount. Please enter a number.\n")
            
            # Provide the user a summary of the transaction and ask confirmation.
            print(f"You are withdrawing £{amount}.\n")
            while True:
                confirmation = input("Confirm ('Yes' or 'No'): ")
                
                if confirmation.lower() in ("no", "exit"):
                    return transaction

                # Create a dictionary with the transaction information, apend it to the DF.
                elif confirmation.lower() == "yes":
                    try:
                        new = {
                        "client_code": user,
                        "date": [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                        "value": [amount],
                        "nature": ["Debit"],
                        "current_balance": [current_balance-amount]
                        }

                        df.reset_index(inplace=True)
                        df = pd.concat([df, pd.DataFrame(new)], axis=0)
                        df.reset_index(drop=True, inplace=True)
                        df.to_json(df_source, indent=4, orient="records")
                    
                        transaction = True
                    
                    except:
                        print("Error on transaction. Call your account manager.\n")
                        transaction = False
                        break
                    
                    return transaction

                else:
                    print("Invalid option.\n")

    except:
        return print("\nOption not available. Insufficient funds.\n")