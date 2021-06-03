import datetime
import unittest

class Account():

    def __init__(self, name, balance = 0, date = None):

        # print("Creating account",name,balance,date)

        self.name = name
        self.balance = 0
        self.date = date
        if date == None:
            self.date = str(datetime.datetime.now())[:10]

        self.transactions = []
        self.transaction("Starting balance", balance)

    def transaction(self, name, amount = 0, date = None):

        self.balance += amount
        if date == None:
            date = str(datetime.datetime.now())[:10]

        self.transactions.append((name, amount, date))

    def __str__(self):

        return "Account Name: {0}\nAccount Balance: {1:.2f}\nAccount Created: {2}\nLast Transaction: {3}\n".format(self.name,self.balance,self.date,self.transactions[-1][2])

    """
    Returns log of transaction in account. By default returns every transaction including creation of account.
    date argument can be given to only access transactions after given date.
    """
    def transaction_log(self, date = None):

        log_index = 0

        max_len_name = 0
        max_len_curr = 0
        for transaction in self.transactions:
            current = transaction
            if len(current[0]) > max_len_name:
                max_len_name = len(current[0])
            if len(str(current[1])) > max_len_curr:
                max_len_curr = len(str(current[1]))

        # In progress
        """
        if date:
            while(self.transactions[log_index][2] < date):
                log_index += 1
        """

        log = ""
        while log_index < len(self.transactions):

            current = self.transactions[log_index]
            text, curr, date = current[0], current[1], current[2]
            #log += f'{text:max_len_name} {curr:max_len_curr}  {date}'
            log += "\nTransaction Name: {0:{1}}\tTransaction Amount: {2:{3}}\tTransaction Date: {4}".format(current[0],max_len_name,current[1],max_len_curr,current[2])
            log_index += 1

        return log

    """
    Helper function for exporting log of transaction to csv
    """
    def transaction_log_csv_format(self):

        log = self.name + "," + str(self.transactions[0][1]) + "," + self.date + ","

        for i in range(1,len(self.transactions)):
            current = self.transactions[i]
            log += "{},{},{},".format(current[0],current[1],current[2])

        return log[:-1] + "\n"


########################### TESTS ##############################################################
class TestMethods(unittest.TestCase):

    def test_empty_init(self):
        account = Account("Savings")
        assert account.name == "Savings"
        assert account.balance == 0
        assert account.date == str(datetime.datetime.now())[:10]
        assert len(account.transactions) == 1
        assert account.transactions[0] == ("Starting balance", 0, str(datetime.datetime.now())[:10])

    def test_init_with_values(self):
        account = Account("Savings", 1400.12)
        assert account.name == "Savings"
        assert account.balance == 1400.12
        assert account.date == str(datetime.datetime.now())[:10]
        assert len(account.transactions) == 1
        assert account.transactions[0] == ("Starting balance", 1400.12, str(datetime.datetime.now())[:10])

    def test_transaction(self):
        account = Account("Savings", 1400.12)
        assert account.name == "Savings"
        assert account.balance == 1400.12
        assert account.date == str(datetime.datetime.now())[:10]
        assert len(account.transactions) == 1
        account.transaction("car payment", -150)
        assert account.name == "Savings"
        assert account.balance == 1250.12
        assert account.date == str(datetime.datetime.now())[:10]
        assert len(account.transactions) == 2
        account.transaction("wages", 250)
        assert account.name == "Savings"
        assert account.balance == 1500.12
        assert account.date == str(datetime.datetime.now())[:10]
        assert len(account.transactions) == 3

    # unreliable test
    # def test_log(self):
    #     account = Account("Savings", 1400.12)
    #     assert account.transaction_log() == "\nTransaction Name: Starting balance\tTransaction Amount: 1400.12\tTransaction Date: " + str(datetime.datetime.now())[:10]
    #     account.transaction("wages", 250)
    #     assert account.transaction_log() == "\nTransaction Name: Starting balance\tTransaction Amount: 1400.12\tTransaction Date: " + str(datetime.datetime.now())[:10] + "\nTransaction Name: wages\tTransaction Amount: 250\tTransaction Date: " + str(datetime.datetime.now())[:10]

if __name__ == '__main__':
    unittest.main()
