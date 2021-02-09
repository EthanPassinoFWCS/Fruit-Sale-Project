import pyodbc
# pip install pyodbc to get this.

class Data:
  def __init__(self, filename):
      self.filename = filename
      self.getdata()

  def getdata(self):
      '''Gets a big list of all the data in the accessdb file. This just might be in the init later on. This will ignore student names.'''
      '''Need https://www.microsoft.com/en-us/download/details.aspx?id=50420 driver to run'''
      conn = pyodbc.connect("DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" + " DBQ=data/" + self.filename)
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
