from datetime import datetime
from bank import Bank

banks = dict()

"""
Gets and validates input from user, ensuring input is a numerical
value, then returns input.
"""
def get_and_validate_currency_input(name):

    entry = None
    while entry == None:
        entry = input(("Please enter a dollar amount to add to {}: ").format(name))

        try:
            entry = float(entry)
        except ValueError:
            print("Error, input {} is not numerical".format(entry))
            entry = None

    return entry

"""
Gets and validates input from user, ensuring input is a proper YYYY-MM-DD format
date, then returns input.
"""
def get_and_validate_date_input():

    entry = None
    while entry == None:
        entry = input("Please enter a date (YYYY-MM-DD): ")

        '''
        Old version of validating date, can be expanded upon if not using datetime module is preferred

        if len(entry) != 10:
            print("Error, input {} is not properly in format YYYY-MM-DD, length does not match".format(entry))
            entry = None
        try:
            int(entry[0:4])
            int(entry[5:7])
            int(entry[8:])
        except ValueError:
            print("Error, input {} is not properly in format YYYY-MM-DD".format(entry))
            '''

        try:
            date = datetime.strptime(entry, '%Y-%m-%d')
        except ValueError:
            print("Error, input {} is not properly in format YYYY-MM-DD".format(entry))
            entry = None


    return str(date)[0:10]

"""
Function to add a banks to the dictionary of all banks.
User can create an empty bank and will be prompted for a name,
or user can import a bank from a file.
"""
def add_bank():

    user_input = None
    choices = {"E","F","R"}
    while user_input != "R":

        print("\nE: create an empty bank")
        print("F: create a bank from a data file")
        print("R: Return to previous choices")

        user_input = input("Please enter your choice: ").upper()

        if user_input not in choices:
            print("Error, {} is not one of the available options".format(user_input))
            user_input = None
        else:
            if user_input == "E":
                name = input("Please enter name of Bank: ")
                bank = Bank(name)
                banks[name] = bank
            elif user_input == "F":
                name = input("Please enter name of Bank: ")
                file_name = input("Please enter name of file: ")
                try:
                    bank = Bank(name, file_name)
                    banks[name] = bank
                    print("Successfully created {} with {} customers!".format(name,len(bank.customers)))
                except FileNotFoundError:
                    print("File {} was not found.".format(file_name))
            return

"""
Function to select a bank from dictionary of banks.
User will recieve a list of all banks, then will be prompted to select one.
"""
def select_bank():

    user_input = None
    while user_input != "R":

        print("List of banks: \n")
        print("\n".join(banks.keys()))
        user_input = input("Please enter the name of a bank, or R to return to previous choices: ")

        if user_input == "R" or user_input == "r":
            return
        else:
            if user_input in banks:
                manage_bank(user_input)
            else:
                print("Error, {} not in list of banks".format(user_input))

"""
Function to manage a bank. User can add a customer using the CLI,
import from a file, or select the option to manage an indiviual customer,
which will call the appropriate function manage_customer.
"""
def manage_bank(bank_name):

    user_input = None
    choices = {"C","F","M","R"}
    while user_input != "R":

        print("Managing {} currently".format(bank_name))
        print("Current funds held: {}".format(banks[bank_name].total_funds()))

        print("\nC: Add a customer from the CLI")
        print("F: Add customer(s) from a file")
        print("M: Manage a customer at this bank")
        print("R: Return to previous choices")

        user_input = input("Please enter your choice: ").upper()

        if user_input not in choices:
            print("Error, {} is not one of the available options".format(user_input))
            user_input = None
        else:
            if user_input == "C":
                name = input("Please enter name of customer: ")
                ID = banks[bank_name].create_customer(name)
                print("Customer successfully created!")
                print(banks[bank_name].customers[ID])
            elif user_input == "F":
                file_name = input("Please enter name of file: ")
                try:
                    previous_customer_num = len(banks[bank_name].customers)
                    banks[bank_name].create_customer_from_csv(file_name)
                    new_customers = len(banks[bank_name].customers) - previous_customer_num
                    print("{} new customers created!".format(str(new_customers)))
                except FileNotFoundError:
                    print("File {} was not found.".format(file_name))
            elif user_input == "M":
                print(banks[bank_name].string_all_customers_no_account_details())

                # print("DEBUG: ", banks[bank_name].customers)
                ID = input("Please enter customer ID: ")
                try:
                    ID = int(ID)
                except ValueError:
                    print("Error, ID {} is not a valid ID".format(ID))
                    break
                # print("DEBUG: ", ID)
                if ID in banks[bank_name].customers:
                    manage_customer(banks[bank_name].customers[ID])
                else:
                    print("Error, ID {} is not used by this bank".format(ID))

"""
Function to manage a customer. User can add an account or funds
to a pre-existing account.
"""
def manage_customer(customer):

    user_input = None
    choices = {"A","B","L","R"}

    while user_input != "R":

        print("\n")
        print(customer)

        print("\nA: Add an account to this customer")
        print("B: Add balance to a pre-existing account")
        print("L: View log of an account's transaction history")
        print("R: Return to previous choices")

        user_input = input("Please enter choice: ").upper()

        if user_input not in choices:
            print("Error, {} is not one of the available options".format(user_input))
            user_input = None
        else:
            if user_input == "A":
                name = input("Please enter name of account: ")
                amount = get_and_validate_currency_input(name)
                try:
                    customer.add_account(name, amount)
                    print("Account successfully created!")
                except KeyError:
                    print("Account already exists, please use add balance option to add to pre-existing account")
            elif user_input == "B":
                name = input("Please enter name of account: ")
                amount = get_and_validate_currency_input(name)
                try:
                    transaction_name = input("Enter note for transaction (optional): ")
                    transaction_name = "N/A" if transaction_name.strip() = "" else transaction_name.rstrip()
                    customer.add_balance(name, amount, transaction_name)
                    print("Funds successfully added!")
                except KeyError:
                    print("Account does not exist, please use add account option to create new account")
            elif user_input == "L":
                name = input("Please enter name of account: ")
                try:
                    print(customer.accounts[name].transaction_log())
                except KeyError:
                    print("Account does not exist")
            elif user_input == "R":
                return

"""
Main/base of program and user access. User can add or access banks, or
export all currently loaded banks into a file that can imported to access data.
"""
if __name__ == '__main__':

    print("Welcome to our Bank Management CLI!")
    user_input = None
    choices = {"A","M","S","Q"}
    while user_input != "Q":

        print("\nA: Add a bank")
        print("M: Manage a bank")
        print("S: Save all bank data")
        print("Q: Quit out of program")

        user_input = input("Please enter your choice: ").upper()

        if user_input not in choices:
            print("Error, {} is not one of the available options".format(user_input))
            user_input = None
        else:
            if user_input == "A":
                add_bank()
            elif user_input == "M":
                if len(banks) > 0:
                    select_bank()
                else:
                    print("Error, no banks are currently loaded.")
            elif user_input == "S":
                for bank in banks:
                    banks[bank].export_to_csv(bank + str(datetime.now())[0:10])
