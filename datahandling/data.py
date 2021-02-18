import os
import json
import pyodbc
# pip install pyodbc to get this.
import sys


class Data:
    def __init__(self, filename, year):
        self.filename = filename
        self.year = year
        self.getdata()
        '''
        self.data is a list that contains each row of the table as a dictionary.
        self.columns is a list that contains each key in each dictionary in the self.data list.
        '''

    def getdata(self):
        '''Gets a big list of all the data in the accessdb file. This just might be in the init later on. This will ignore student names.'''
        '''Need https://www.microsoft.com/en-us/download/details.aspx?id=54920 to run. Make sure it is the same bit version as python. If it doesn't say which it is, it is 32 bit.'''
        try:
            conn = pyodbc.connect("DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" + " DBQ=data/" + self.filename + ";")
        except pyodbc.InterfaceError:
            print("An error has occured that has caused us not to be able to access the database file to get the data. This more than likely means that you do not have the correct stuff installed properly to access these files. Your python bit version and the bit version of the Microsoft Access Driver must be the same.")
            # Checks if the system is 64 bit or 32 bit.
            is64bit = sys.maxsize > 2**32
            if is64bit:
                print("The python version you were running was 64 bit. Download and install the 'accessdatabaseengine_X64.exe' file from here: https://www.microsoft.com/en-us/download/details.aspx?id=54920")
            else:
                print("The python version you were running was 32 bit. Download and install the 'accessdatabaseengine.exe' file from here: https://www.microsoft.com/en-us/download/details.aspx?id=54920")
            exit(-1)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM FruitSale")
        data = []
        self.columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            entry = [r for r in row]
            fixed_entry = {}
            for c in self.columns:
                if c == "teacherCode" or c == "StudentLastName" or c == "StudentFirstName" or c == "SmallBaskets" or c == "LargeBaskets":
                    continue
                fixed_entry[c] = entry[self.columns.index(c)]
            data.append(fixed_entry)
        self.data = data
        cursor.close()
        conn.close()
        with open(f"prices/{self.year}.json") as pr:
            try:
                self.prices = json.load(pr)
                if len(self.prices) == 0:
                    self.prices = {"ERR": None}
            except FileNotFoundError:
                print(f"There was no price for the year {self.year}")
                self.prices = {"ERR": None}

    def getFruitData(self, fruit):
        '''This goes through and gets all data about a fruit, its name and number of buys'''
        '''self.data will contain the data'''
        if len(self.data) == 0:
            print("This object contains no data.")
            return -2
        if fruit not in self.columns or fruit == "Sheet" or fruit == "AmountOwed" or fruit == "ID" or fruit == "teacherCode" or fruit == "StudentLastName" or fruit == "StudentFirstName" or fruit == "SmallBaskets" or fruit == "LargeBaskets":
            print("Error: This fruit/basket is not in the data.")
            return -1
        total = 0
        for data_dict in self.data:
            if data_dict[fruit] is None:
                continue
            try:
                total += int(data_dict[fruit])
            except ValueError:
                continue
        return total

    def getTotalDictionary(self):
        '''This returns a dictionary that contains each fruits total.'''
        dict = {}
        for fruit in self.columns:
            if fruit == "Sheet" or fruit == "AmountOwed" or fruit == "ID" or fruit == "teacherCode" or fruit == "StudentLastName" or fruit == "StudentFirstName" or fruit == "SmallBaskets" or fruit == "LargeBaskets":
                continue
            dict[fruit] = self.getFruitData(fruit)
        return dict

    def getFruitCost(self, fruit):
        '''Gets the cost of the fruit specified (if it can)'''
        if "ERR" in list(self.prices.keys()):
            return 0
        for key in list(self.prices.keys()):
            if key.lower() == fruit.lower():
                return self.prices[key]
        return 0

    def getTotalCosts(self):
        """This returns a dictionary. Each key is a fruit that contains a value of the total cost gotten from that fruit from this year."""
        totals = {}
        fruitsGotten = self.getTotalDictionary()
        for col in self.columns:
            if col == "Sheet" or col == "AmountOwed" or col == "ID" or col == "teacherCode" or col == "StudentLastName" or col == "StudentFirstName" or col == "SmallBaskets" or col == "LargeBaskets":
                continue
            totals[col] = self.getFruitCost(col) * fruitsGotten[col]
        return totals

data = []
for dbfile in os.listdir("data/"):
    if dbfile.split(".")[-1] == "accdb":
        try:
            year_int = int(dbfile[0:4])
        except ValueError:
            print(f"The first 4 characters of the file name must be the year in numbers. Please fix the file {dbfile} to support this format.")
            continue
        data.append(Data(dbfile, year_int))
    else:
        print(f"The file {dbfile} is not a '.accdb' file. It must be a '.accdb' file. Skipped this file.")
