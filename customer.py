import datetime
import unittest
from account import Account

"""
This class represents a customer at a bank.
Customers have a name, ID, date of account creation and accounts assoctiated with them.
Customers can add accounts or add to the balance of any account they own.
"""
class Customer():

    def __init__(self, name, ID, date  = None, accounts = None):

        # print("Creating customer",name,ID,date)

        self.name = name
        self.ID = ID
        self.date = date
        self.accounts = dict()

        if date == None:
            self.date = str(datetime.datetime.now())[:10]

        if accounts:
            for key in accounts:
                self.accounts[key] = accounts[key]

    """
    Returns a string of customer details with details of every individual account they own
    """
    def __str__(self):
        text = "ID: {}\nName: {}\nStart of Service: {}\nAccounts:\n\n".format(self.ID,self.name,self.date)
        for key in self.accounts:
            text += str(self.accounts[key]) + "\n"
        return text

    """
    Returns a string of customer details without details of every individual account they own
    """
    def string_no_account_details(self):
        return "ID: {}\nName: {}\nStart of Service: {}\nNumber of Accounts: {}\n".format(self.ID,self.name,self.date,len(self.accounts))

    """
    Returns sum of all accounts' balances
    """
    def total_funds(self):

        total = 0
        for account in self.accounts:
            total += self.accounts[account].balance
        return total

    """
    Adds balance to a pre-existing account. Throws a KeyError if account does not exist
    """
    def add_balance(self, account, amount = 0.00, transaction_name = "N/A"):
        if account in self.accounts:
            self.accounts[account].transaction(transaction_name, amount)
        else:
            raise KeyError("Account does not exist")

    """
    Adds account to customer's accounts. Throws a KeyError if account already exists
    """
    def add_account(self, account, amount = 0.00):
        if account in self.accounts:
            raise KeyError("Account already exists")
        else:
            self.accounts[account] = Account(account, amount)

########################### TESTS ##############################################################
class TestMethods(unittest.TestCase):

    def test_empty_init(self):
        cust = Customer("Jon", 14)
        assert cust.name == "Jon"
        assert cust.ID == 14
        assert cust.date == str(datetime.datetime.now())[:10]
        assert cust.total_funds() == 0

    def test_init_with_values(self):
        acc = Account("savings", 500)
        cust = Customer("Jane", 16, "2020-05-01", {"savings":acc})
        assert cust.name == "Jane"
        assert cust.ID == 16
        assert cust.date == "2020-05-01"
        assert cust.total_funds() == 500

    def test_add_balance(self):
        acc = Account("savings", 500)
        cust = Customer("Jane", 16, "2020-05-01", {"savings":acc})
        assert cust.accounts["savings"].balance == 500
        cust.add_balance("savings")
        assert cust.accounts["savings"].balance == 500
        cust.add_balance("savings",100)
        assert cust.accounts["savings"].balance == 600

        assert cust.total_funds() == 600

        with self.assertRaises(KeyError):
            cust.add_balance("checking",500)

    def test_add_account(self):
        acc = Account("savings", 500)
        cust = Customer("Jane", 16, "2020-05-01", {"savings":acc})
        assert cust.accounts["savings"].balance == 500
        assert cust.total_funds() == 500
        cust.add_account("checking")
        assert cust.accounts["savings"].balance == 500 and cust.accounts["checking"].balance == 0
        assert cust.total_funds() == 500
        cust.add_account("401k",6000.00)
        assert cust.accounts["savings"].balance == 500 and cust.accounts["checking"].balance == 0 and cust.accounts["401k"].balance == 6000
        assert cust.total_funds() == 6500

        with self.assertRaises(KeyError):
            cust.add_account("checking",500)

    def test_total_funds(self):
        cust = Customer("Jon", 14)
        cust.total_funds() == 0
        cust.add_account("checking")
        cust.total_funds() == 0
        cust.add_account("401k",6000.00)
        cust.total_funds() == 6000
        cust.add_account("Savings",300.06)
        cust.total_funds() == 6300.06


if __name__ == '__main__':
    unittest.main()
    # test_accounts = {"checking": 500.00, "savings": 5000.00}
    #
    # test_cust = Customer("Sam",0, accounts = test_accounts)
    # print(test_cust)
