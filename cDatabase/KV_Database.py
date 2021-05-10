import os, importlib

class KV_Database:
  db = dict()
  path = str()

  def exist(self): return os.path.isfile(self.path)

  def create_file(self):
    try:
      file = open(self.path, "w+")
      file.write("DataBase = {}")
      file.close()
      self.db = {}
    except FileNotFoundError as ex:
      print("Error Creating: " + str(ex))
      
  def load(self):
    try:
      dir = '.'.join(self.path.split('/'))
      db = importlib.import_module(dir[:-3])
      self.db = db.DataBase
    except ImportError as ex:
      print("Error Loading: " + str(ex))

  def __init__(self, path):
    self.path = "databases/" + path + ".py"
    if self.exist(): self.load()
    else: self.create_file()
   
  def get(self, key): return self.db[key]
  def keys(self): return list(self.db.keys())
  def items(self): return list(self.db.items())
  def values(self): return list(self.db.values())
  def count(self, key): return (key in self.db.keys())
 
  def save(self):
    file = open(self.path, "w+")
    file.write("DataBase = ")
    file.write(str(self.db))
    file.close()