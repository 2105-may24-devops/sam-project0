from datetime import datetime
from os import listdir
from bank import Bank
import sys
import unittest

banks = dict()
data_location = "data/"

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
Helper function to increase readability of other functions in program by
removing the block of print statements at the start of function and putting them
in this function.
"""
def print_choices(function):

    if function == "add_bank":
        print("\nE: create an empty bank")
        print("F: create a bank from a data file")
        print("R: Return to previous choices")
    elif function == "manage_bank":
        print("\nC: Add a customer from the CLI")
        print("F: Add customer(s) from a file")
        print("M: Manage a customer at this bank")
        print("R: Return to previous choices")
    elif function == "manage_customer":
        print("\nA: Add an account to this customer")
        print("B: Add balance to a pre-existing account")
        print("L: View log of an account's transaction history")
        print("R: Return to previous choices")
    else:
        print("\nA: Add a bank")
        print("L: Load all banks in logs")
        print("M: Manage a bank")
        print("S: Save all bank data")
        print("Q: Quit out of program")

"""
Function to add a banks to the dictionary of all banks.
User can create an empty bank and will be prompted for a name,
or user can import a bank from a file.
"""
def add_bank():

    user_input = None
    choices = {"E","F","R"}
    while user_input != "R":

        print_choices("add_bank")

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
                file_name = input("Please enter name of data file: ")
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
        print("\n")

        user_input = input("Please enter the name of a bank, or R to return to previous choices: ")

        if user_input == "R" or user_input == "r":
            return
        else:
            if user_input in banks:
                manage_bank(user_input)
            else:
                print("Error, {} not in list of banks".format(user_input))

"""
Function to manage the input commands of both the bank and customer
user_permisions is a string of who the user is bank or customer
Will return and int of which option they chose

Helper function created by Andrew during training. I like the way he dealt
with more of the repeated code in the two functions, but he only handles 2
functions. Will try to implement his idea with user_input in the print_choices
function I created to address the same issue.
"""
def check_user_input(user_permisions):
    user_input = None
    if user_permisions.lower() == "bank":
        choices = {"C","F","M","R"}
        print("\nC: Add a customer from the CLI")
        print("F: Add customer(s) from a file")
        print("M: Manage a customer at this bank")
        print("R: Return to previous choices")

    elif user_permisions.lower() == "customer":
        choices = {"A","B","L","R"}
        print("\nA: Add an account to this customer")
        print("B: Add balance to a pre-existing account")
        print("L: View log of an account's transaction history")
        print("R: Return to previous choices")

    else:
        print("Error, {} is not one of the available options".format(user_permisions))
    user_input = input("Please enter your choice: ").upper()
    if user_input not in choices:
        print("Error, {} is not one of the available options".format(user_input))
        user_input = None
    return user_input


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
        print("Current funds held: {0:.2f}".format(banks[bank_name].total_funds()))

        print_choices("manage_bank")

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
                file_name = data_location + input("Please enter name of data file: ")
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

        print_choices("manage_customer")

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
                    transaction_name = "N/A" if transaction_name.strip() == "" else transaction_name.rstrip()
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

########################### TESTS ##############################################################
class TestUserInput(unittest.TestCase):

    def test_text_input(self):
        print("Ran Test",test_num)
        if test_num == 1:
            assert len(banks) == 1
            assert len(banks["Bank of Poor Financial Choices"].customers) == 1
            assert banks["Bank of Poor Financial Choices"].customers[0].name == "Bad Luck Laurence"
            assert banks["Bank of Poor Financial Choices"].customers[0].accounts["Savings"].balance == 50
        if test_num == 2:
            assert len(banks) == 1
            assert len(banks["MTB"].customers == 3)
            assert len(banks["MTB"].customers[0].accounts == 2)
            assert banks["MTB"].total_funds() == 7892.25

"""
Main/base of program and user access. User can add or access banks, or
export all currently loaded banks into a file that can imported to access data.
"""
if __name__ == '__main__':

    test_time = False
    test_num = 0
    print("Welcome to our Bank Management CLI!")
    user_input = None
    choices = {"A","L","M","S","Q","TEST_RUN1","TEST_RUN2"}
    while user_input != "Q":

        print_choices("")

        user_input = input("Please enter your choice: ").upper()

        if user_input not in choices:
            print("Error, {} is not one of the available options".format(user_input))
            user_input = None
        else:
            if user_input == "A":
                add_bank()
            elif user_input == "L":
                files = listdir(data_location)
                previous_bank_num = len(banks)
                for file in files:
                    bank_name = file[:-4]
                    banks[bank_name] = Bank(bank_name)
                    print("Loading",bank_name)
                    try:
                        banks[bank_name].create_customer_from_csv(data_location + file)
                    except FileNotFoundError:
                        print("File {} was not found.".format(file_name))

                new_banks = len(banks) - previous_bank_num
                print("{} banks loaded".format(str(new_banks)))

            elif user_input == "M":
                if len(banks) > 0:
                    select_bank()
                else:
                    print("Error, no banks are currently loaded.")
            elif user_input == "S":
                for bank in banks:
                    banks[bank].export_to_csv(data_location + bank + ".csv")
            elif user_input == "TEST_RUN1" or user_input == "TEST_RUN2":
                test_time = True
                test_num = user_input[-1:]

    if test_time:
        unittest.main()
