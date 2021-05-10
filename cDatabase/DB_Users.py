from cDatabase.KV_Database import KV_Database

class DB_Users(KV_Database):
    def __init__(self, path):
        super().__init__(path)

    def find_id(self, handle):
        for (k, v) in self.db.items():
            if (v == handle): return k
        return None

    def find_handle(self, _id):
        if (_id in self.db.keys()): return self.db[_id]
        return None

    def is_taken_id(self, user):
        return (user.id in self.db.keys())

    def is_taken_handle(self, user):
        for (k, v) in self.db.items():
            if (v == user.handle): return True
        return False

    def is_registered(self, user):
        for (k, v) in self.db.items():
            if (k == user.id and v == user.handle): return True
        return False

    def register(self, user):
        if (self.is_taken_handle(user)): return False
        if (self.is_taken_id(user)): return False
        self.db[user.id] = user.handle
        self.save()
        return True

    def change_handle(self, user, new_handle):
        self.db[user.id] = new_handle
        self.save()
        return True

    def remove_user(self, user):
        if (not self.is_registered(user)): return True
        del(self.db[user.id])
        self.save()
        return True