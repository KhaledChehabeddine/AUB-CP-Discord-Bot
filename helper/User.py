from cDatabase.DB_Users import DB_Users

database_users = DB_Users("db_users")

# ------------------------------------ { User } ------------------------------------ # 
    # ------------------ [ __init__() ] ------------------ # 
        # Checks if 
class User:
    id = handle = None

    def __init__(self, id = '', handle = ''):
        if (id != '' and handle != ''): self.id, self.handle = id, handle
        elif (id != ''): 
            self.id = id
            self.handle = database_users.find_handle(id)
        elif (handle != ''): 
            self.id = database_users.find_id(handle)
            self.handle = handle

    def is_admin(self):
        if self.id in [
            '763289145288032268',
            '763319277540605972',
            '763345404674048020',
            '402887362046066698'
        ]: return True
        return False

    def tag(self):
        return '<@!' + str(self.id) + '>'

    def is_taken_id(self):
        if (self.id == None): return True
        return database_users.is_taken_id(self)

    def is_taken_handle(self):
        if (self.handle == None): return True
        return database_users.is_taken_handle(self)

    def is_registered(self):
        if (self.id == None or self.handle == None): return False
        return database_users.is_registered(self)

    def register(self):
        if (self.id == None or self.handle == None): return False
        return database_users.register(self)

    def change_handle(self, new_handle):
        if (self.handle == new_handle): return False
        if (not self.is_registered()): return False
        self.handle = new_handle
        return database_users.change_handle(self, new_handle)

    def delete(self):
        # Add remove from contests
        if (self.id == None or self.handle == None): return False
        return database_users.remove_user(self)

    def __str__(self):
        return "User: " + str(self.id) + ' ' + str(self.handle)