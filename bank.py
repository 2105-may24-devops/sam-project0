import unittest
from customer import Customer
from account import Account

"""
This class represents a bank.
Banks have a name and customers, stored as a dictionary.
Banks can add customers or read in data files to add customers.
"""
class Bank():

    def __init__(self,name,file = None):

        self.name = name
        self.nextID = 0
        self.customers = dict()
        if file:
            self.create_customer_from_csv(file)

    def __str__(self):
        return "{}, customers: {}".format(self.name,len(self.customers))

    """
    Reads in csv file and adds customers to bank's dictionary of customers
    """
    def create_customer_from_csv(self,file):
        f = open(file)

        data = f.readlines()

        if data == []:
            f.close()
            return

        next_customer_start = 0
        for i in range(next_customer_start,len(data)):
            if data[i] == "\n":
                self.create_customer_from_csv_section(data[next_customer_start:i])
                next_customer_start = i+1

        self.create_customer_from_csv_section(data[next_customer_start:])

        f.close()

    """
    Adds customer from single line of csv file
    """
    def create_customer_from_csv_section(self,data):

        if data == []:
            return

        new_accounts = dict()
        for i in range(1,len(data)):
            line = data[i].rstrip().split(",")
            new_account = Account(line[0],float(line[1]),line[2])
            for j in range(3,len(line),3):
                new_account.transaction(line[j],float(line[j+1]),line[j+2])
            new_accounts[line[0]] = new_account

        line = data[0].rstrip().split(",")
        self.create_customer(line[1],line[0], date = line[2], accounts = new_accounts)

        # data = data.rstrip().split(",")
        # if data[0] and data[0] in self.customers:
        #     raise KeyError("Account with ID {} already exists".format(data[0]))
        # else:
        #     accounts = dict()
        #     for i in range(3,len(data),2):
        #         accounts[data[i]] = float(data[i+1])
        #
        #     self.create_customer(data[1],data[0],data[2],accounts, True)

    """
    Adds customer to bank's dictionary of customers based on given data, and returns ID of customer
    """
    def create_customer(self, name, ID = None, date = None, accounts = None, auto_fill_ID = True):

        if ID and ID in self.customers:
            if auto_fill_ID:
                while self.nextID in self.customers:
                    self.nextID += 1
                ID = self.nextID
                self.nextID += 1
            else:
                raise KeyError("Account with ID {} already exists".format(ID))
        else:
            ID = self.nextID
            self.nextID += 1

        new_cust = Customer(name, ID, date, accounts)
        self.customers[new_cust.ID] = new_cust
        return ID

    """
    Returns a string of the bank's name, number of customers and total funds held by
    bank, measured as a total of it's customers' accounts' funds
    """
    def __str__(self):

        return "Name: {0}\nNumber of Customers: {1}\nTotal funds held: {2:.2f}\n".format(self.name,len(self.customers),self.total_funds())

    """
    Returns total funds held by bank, calculated as the sum of all customers' accounts' balances
    """
    def total_funds(self):

        total = 0
        for customer in self.customers:
            total += self.customers[customer].total_funds()

        return total

    """
    Returns a string of all customers and without specific account details
    """
    def string_all_customers_no_account_details(self):

        text = ""
        for customer in self.customers:
            text += (self.customers[customer].string_no_account_details())

        return text

    """
    Returns a string of all customers and with specific account details
    """
    def string_all_customers_with_account_details(self):

        text = ""
        for customer in self.customers:
            text += (str(self.customers[customer]))
        return text

    """
    Creates a file to save all bank data, which can then be used by the
    create_customer_from_csv method to load back customers
    """
    def export_to_csv(self, file_name):

        f = open(file_name, 'w')
        for customer in self.customers:
            current = self.customers[customer]
            line = str(current.ID) + ',' + str(current.name) + ',' + str(current.date) + "\n"

            if len(current.accounts) > 0:
                for account in current.accounts:
                    line += current.accounts[account].transaction_log_csv_format()

            f.write(line + "\n")

        f.close()

########################### TESTS ##############################################################
class TestMethods(unittest.TestCase):

    def test_empty_init(self):
        bank = Bank("Bank of America")
        assert bank.name == "Bank of America"
        assert len(bank.customers) == 0
        self.assertDictEqual(bank.customers, {})

    def test_init_with_file(self):
        bank = Bank("Bank of America", "test_data2.csv")
        assert bank.name == "Bank of America"
        assert len(bank.customers) == 3

        # All data is tested against test_data2.csv
        assert bank.customers[0].name == "Sam"
        assert bank.customers[1].name == "Joe"
        assert bank.customers[2].name == "Jane"

        assert bank.customers[0].ID == 0
        assert bank.customers[1].ID == 1
        assert bank.customers[2].ID == 2

        assert bank.customers[0].date == "2014-08-01"
        assert bank.customers[1].date == "2013-09-16"
        assert bank.customers[2].date == "2020-06-24"

        assert bank.customers[0].total_funds() == 7641.26
        assert bank.customers[1].total_funds() == 250.99
        assert bank.customers[2].total_funds() == 0

        with self.assertRaises(FileNotFoundError):
            bank2 = Bank("fake name", "non-existant_file.csv")

    def test_create_customer(self):
        bank = Bank("Bank of America", "test_data2.csv")
        bank.create_customer("George")
        assert len(bank.customers) == 4
        assert bank.nextID == 4

        assert 3 in bank.customers
        assert bank.customers[3].name == "George"
        assert bank.customers[3].ID == 3
        self.assertDictEqual(bank.customers[3].accounts, {})

    def test_total_funds(self):

        bank = Bank("Bank of America", "test_data2.csv")
        assert bank.total_funds() == 7892.25
        bank.create_customer("Max", accounts = {"Holdings": Account("Holdings", 46.24)})
        assert bank.total_funds() == 7938.49

    def test_export_to_csv(self):

        bank = Bank("Bank of America", "test_data2.csv")
        bank.create_customer("Max", accounts = {"Holdings": Account("Holdings", 46.24)})
        bank.export_to_csv("test_export.csv")
        bank2 = Bank("Bank of South Canada", "test_export.csv")
        assert bank2.name == "Bank of South Canada"
        assert len(bank.customers) == 4

        # All data is tested against test_export.csv
        assert bank2.customers[0].name == "Sam"
        assert bank2.customers[1].name == "Joe"
        assert bank2.customers[2].name == "Jane"
        assert bank2.customers[3].name == "Max"

        assert bank2.customers[0].ID == 0
        assert bank2.customers[1].ID == 1
        assert bank2.customers[2].ID == 2
        assert bank2.customers[3].ID == 3

        assert bank2.customers[0].date == "2014-08-01"
        assert bank2.customers[1].date == "2013-09-16"
        assert bank2.customers[2].date == "2020-06-24"

        assert bank2.customers[0].total_funds() == 7641.26
        assert bank2.customers[1].total_funds() == 250.99
        assert bank2.customers[2].total_funds() == 0
        assert bank2.customers[3].total_funds() == 46.24

if __name__ == '__main__':
    unittest.main()

    # bank = Bank("Bank of America", "test_data2.csv")
    # bank.create_customer("Max", accounts = {"Holdings": Account("Holdings", 46.24)})
    # bank.export_to_csv("test_export.csv")
    # bank2 = Bank("Bank of South Canada", "test_export.csv")
