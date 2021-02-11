import pyodbc
# pip install pyodbc to get this.
import sys
class Data:
    def __init__(self, filename):
        self.filename = filename
        self.getdata()

    def getdata(self):
        '''Gets a big list of all the data in the accessdb file. This just might be in the init later on. This will ignore student names.'''
        '''Need https://www.microsoft.com/en-us/download/details.aspx?id=54920 to run. Make sure it is the same bit version as python. If it doesn't say which it is, it is 32 bit.'''
        try:
            conn = pyodbc.connect("DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" + " DBQ=data/" + self.filename + ";")
        except pyodbc.InterfaceError:
            print("An error has occured that has caused us not to be able to access the database file to get the data. This more than likely means that you do not have the correct stuff installed properly to access these files. Your python bit version and the bit version of the Microsoft Access Driver must be the same.")
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
                if c == "teacherCode" or c == "StudentLastName" or c == "StudentFirstName":
                    continue
                fixed_entry[c] = entry[self.columns.index(c)]
            data.append(fixed_entry)
        self.data = data


    def getFruitData(self, fruit):
        '''This goes through and gets all data about a fruit, its name and number of buys'''
        '''self.data will contain the data'''

    def orderFruits(self):
        '''This will return a list with the fruits ordered from most bought from to least bought'''


d = Data("2016AnthisFruit.accdb", "2017AnthisFruit.accdb", "2018AnthisFruit.accdb", "2019AnthisFruit.accdb", "2020AnthisFruit1.accdb")

print(d.data)
