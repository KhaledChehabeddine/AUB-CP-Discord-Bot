from cDatabase.KV_Database import KV_Database

class DB_Algorithm(KV_Database):
    def __init__(self, path): super().__init__(path)

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