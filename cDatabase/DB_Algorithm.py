import importlib
from cDatabase.KV_Database import KV_Database

class DB_Algorithm(KV_Database):
    def __init__(self, path): 
        super().__init__(path)
        file_path = '.'.join(self.path.split('/'))[:-3]
        try:
            db = importlib.import_module(file_path)
            self.mp = db.Mapping
        except Exception:
            fs = open(self.path, "a")
            fs.write("\n\nMapping = {}")
            fs.close()
            self.mp = {}

    def save(self):
        file = open(self.path, "w")
        file.write("DataBase = " + str(self.db))
        file.write("\n\nMapping = " + str(self.mp))
        file.close()

    def find_algo(self, algorithm, language):
        algorithm = algorithm.lower()
        language = language.lower()
        if algorithm not in self.db.keys(): return False
        if language not in self.db.get(algorithm): return False
        return True
    
    def add_algo(self, algorithm, language):
        algorithm = algorithm.lower()
        language = language.lower()

        if self.find_algo(algorithm, language): return False

        if algorithm in self.db.keys(): self.db[algorithm] += [language]
        else: self.db[algorithm] = [language]

        self.save()

        return True

    def del_algo(self, algorithm, language):
        algorithm = algorithm.lower()
        language = language.lower()

        self.db[algorithm].remove(language)
        if len(self.db[algorithm]) == 0: self.delete_key(algorithm)
        self.save()

    def find_mapping(self, algorithm, alias):
        algorithm, alias = algorithm.lower(), alias.lower()
        if algorithm not in self.mp.keys(): return False
        if alias not in self.mp.get(algorithm): return False
        return True

    def add_mapping(self, algorithm, alias):
        algorithm, alias = algorithm.lower(), alias.lower()

        if self.find_mapping(algorithm, alias): return False

        if algorithm in self.mp.keys(): self.mp[algorithm] += [alias]
        else: self.mp[algorithm] = [alias]

        self.save()

        return True

    def get_mappings(self, algorithm):
        algorithm = algorithm.lower()
        if algorithm in self.mp.keys(): return self.mp[algorithm]
        else: return []

    def is_valid_mapping(self, algorithm, keyword):
        algorithm, keyword = algorithm.lower(), keyword.lower()
        if keyword in algorithm: return True
        for alias in self.get_mappings(algorithm):
            if keyword in alias: return True
        return False